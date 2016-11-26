import hashlib
import json

import boto.elastictranscoder
import boto3


def getChildren(folder):
    client = boto3.client('s3')
    prefix = folder['url_ext']
    print('PREFIX', prefix)

    cloudfront_prefix = 'http://d2zi1eot6cm0a8.cloudfront.net/'

    kwargs = {
        'Bucket': 'streamingproject.hls',
        'MaxKeys': 10,
        'Prefix': prefix
    }

    response = client.list_objects_v2(**kwargs)
    print(response.keys())

    if 'Contents' in response.keys():
        objects = [obj for obj in response['Contents']]
        keys = [obj['Key'] for obj in objects]
        for key in keys:
            print('KEY:', key)
            section = key[len(prefix):].split('/')[0]
            print('SECTION:', section)
            if section not in folder['children'].keys():
                folder['children'][section] = {
                    'name': section,
                    'url_ext': folder['url_ext'] + section,
                    'url': folder['url'] + section,
                    'children': {}
                }
                getChildren(folder['children'][section])


def getFileTree():
    client = boto3.client('s3')

    cloudfront_prefix = 'http://d2zi1eot6cm0a8.cloudfront.net/'

    kwargs = {
        'Bucket': 'streamingproject.hls',
        'MaxKeys': 10,
        'Prefix': 'transcoded/'
    }
    response = client.list_objects_v2(**kwargs)
    objects = [obj for obj in response['Contents']]
    keys = [obj['Key'] for obj in objects]
    explorer = {}
    for key in keys:
        section = key.split('/')[0]
        if section not in explorer.keys():
            explorer[section] = {
                'name': section,
                'url_ext': section,
                'url': cloudfront_prefix + section,
                'children': {}
            }
            getChildren(explorer[section])

    print("EXPLORER:", explorer)
    return explorer


def create_job():
    # This is the ID of the Elastic Transcoder pipeline that was created when
    # setting up your AWS environment:
    # http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/sample-code.html#python-pipeline
    pipeline_id = '1479630575829-7p3ujm'

    # This is the name of the input key that you would like to transcode.
    input_key = 'Modern.Family.S04E20.720p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mkv'

    # Region where the sample will be run
    region = 'us-west-2'

    # HLS Presets that will be used to create an adaptive bitrate playlist.
    hls_64k_audio_preset_id = '1351620000001-200071'
    hls_0400k_preset_id = '1351620000001-200050'
    hls_0600k_preset_id = '1351620000001-200040'
    hls_1000k_preset_id = '1351620000001-200030'
    hls_1500k_preset_id = '1351620000001-200020'
    hls_2000k_preset_id = '1351620000001-200010'

    # HLS Segment duration that will be targeted.
    segment_duration = '10'

    # All outputs will have this prefix prepended to their output key.
    output_key_prefix = 'transcoded/MFSE3E20/'

    # Creating client for accessing elastic transcoder
    transcoder_client = boto.elastictranscoder.connect_to_region(region)

    # Setup the job input using the provided input key.
    job_input = {'Key': input_key}

    # Setup the job outputs using the HLS presets.
    output_key = hashlib.sha256(input_key.encode('utf-8')).hexdigest()
    hls_audio = {
        'Key': 'hlsAudio/' + output_key,
        'PresetId': hls_64k_audio_preset_id,
        'SegmentDuration': segment_duration
    }
    hls_400k = {
        'Key': 'hls0400k/' + output_key,
        'PresetId': hls_0400k_preset_id,
        'SegmentDuration': segment_duration
    }
    hls_600k = {
        'Key': 'hls0600k/' + output_key,
        'PresetId': hls_0600k_preset_id,
        'SegmentDuration': segment_duration
    }
    hls_1000k = {
        'Key': 'hls1000k/' + output_key,
        'PresetId': hls_1000k_preset_id,
        'SegmentDuration': segment_duration
    }
    hls_1500k = {
        'Key': 'hls1500k/' + output_key,
        'PresetId': hls_1500k_preset_id,
        'SegmentDuration': segment_duration
    }
    hls_2000k = {
        'Key': 'hls2000k/' + output_key,
        'PresetId': hls_2000k_preset_id,
        'SegmentDuration': segment_duration
    }
    job_outputs = [hls_audio, hls_400k, hls_600k, hls_1000k, hls_1500k, hls_2000k]

    # Setup master playlist which can be used to play using adaptive bitrate.
    playlist = {
        'Name': 'hls_' + output_key,
        'Format': 'HLSv3',
        'OutputKeys': map(lambda x: x['Key'], job_outputs)
    }

    # Creating the job.
    create_job_request = {
        'pipeline_id': pipeline_id,
        'input_name': job_input,
        'output_key_prefix': output_key_prefix + output_key + '/',
        'outputs': job_outputs,
        'playlists': [playlist]
    }
    create_job_result = transcoder_client.create_job(**create_job_request)
    print('HLS job has been created: ', json.dumps(create_job_result['Job'], indent=4, sort_keys=True))
