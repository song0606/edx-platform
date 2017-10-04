"""
API utils in order to communicate to edx-video-pipeline.
"""
from django.core.exceptions import ObjectDoesNotExist

from openedx.core.djangoapps.video_pipeline.models import VideoPipelineIntegration
from openedx.core.djangoapps.video_pipeline.utils import create_video_pipeline_api_client


def update_3rd_party_transcription_service_credentials(**credentials_payload):
    """
    Updates the 3rd Party Transcription Service's Credentials.

    Arguments:
        credentials_payload(dict): A payload containing org, provider and its credentials.

    Returns:
        A tuple containing whether the credentials update was a success or not and the response payload.
    """
    is_updated, response_content = False, ''
    pipeline_integration = VideoPipelineIntegration.current()
    if pipeline_integration.enabled:
        try:
            video_pipeline_user = pipeline_integration.get_service_user()
        except ObjectDoesNotExist:
            return False, response_content

        client = create_video_pipeline_api_client(user=video_pipeline_user, api_url=pipeline_integration.api_url)
        response = client.transcript_credentials.post(credentials_payload)
        is_updated, response_content = response.status_code == 200, response.content

    return is_updated, response_content
