import logging
import time
from typing import Any, Optional, Dict, List

import broadscope_bailian
from pydantic.class_validators import root_validator

from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.utils import enforce_stop_tokens

logger = logging.getLogger(__name__)


class AccessTokenManager:
    """ Token manager for cache token """

    def __init__(self, access_key_id: str,
                 access_key_secret: str,
                 agent_key: str):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.agent_key = agent_key

        self.token = None
        self.expired_time = None

    def get_token(self):
        """ get token if not created or expired """

        timestamp = int(time.time())
        if self.token is None or self.expired_time is None or (self.expired_time - 600) < timestamp:
            self.create_token()

        return self.token

    def create_token(self):
        """ create api token """

        client = broadscope_bailian.AccessTokenClient(access_key_id=self.access_key_id,
                                                      access_key_secret=self.access_key_secret)
        self.token, self.expired_time = client.create_token(agent_key=self.agent_key)


class BroadscopeBailian(LLM):
    """Wrapper of Broadscope Bailian LLM for langchain.

    To use, you should have the `` broadscope_bailian `` python packet installed, and then
    pass the parameters to constructor before calling functions.

    Example:
        .. code-block:: python

            from broadscope_bailian_llm import BroadscopeBailian
            llm = BroadscopeBailian()
            llm("1+1=?")
    """

    client: Any

    access_key_id: str
    """ access key of aliyun account"""

    access_key_secret: str
    """ access key secret of aliyun account """

    agent_key: str
    """ agent key for broad scope business scope """

    app_id: str
    """ id of broadscope bailian application """
    top_p: Optional[float] = None
    """Total probability mass of tokens to consider at each step."""
    stream: bool = False
    """Whether to stream the results or not."""

    token_manager: AccessTokenManager = None

    def __call__(self, *args, **kwargs):
        self._init()
        return super().__call__(*args, **kwargs)

    def _init(self):
        if self.token_manager is None:
            self.token_manager = AccessTokenManager(access_key_id=self.access_key_id,
                                                    access_key_secret=self.access_key_secret,
                                                    agent_key=self.agent_key)

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "broadscope_bailian"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """ Validate input params """

        # Skip creating new client if passed in constructor
        if values["client"] is not None:
            return values

        try:
            import broadscope_bailian
            values["client"] = broadscope_bailian.Completions()

        except ImportError:
            raise ModuleNotFoundError(
                "Could not import broadscope_bailian python package. "
                "Please install it with `pip install broadscope_bailian`."
            )

        return values

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        """Call out to broadscope bailian text generation service.

        """
        self._init()
        broadscope_bailian.api_key = self.token_manager.get_token()

        try:
            session_id = kwargs.get("session_id")
            response = self.client.call(app_id=self.app_id, prompt=prompt, stream=self.stream, session_id=session_id)
            if not response.get("Success"):
                raise RuntimeError(response.get("Message"))

            text = response.get("Data", {}).get("Text")

        except Exception as e:
            raise RuntimeError(f"Error raised by broadscope service: {e}")

        if stop is not None:
            text = enforce_stop_tokens(text, stop)

        return text
