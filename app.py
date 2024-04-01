import json
import os
import time

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION)

transcribe = boto3.client('transcribe')
transcribe_client = boto3.client("transcribe", aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
transc_job_name = "DEP-transcript-job"


@app.route('/transcribe', methods=['POST'])
def transcribe():
    print("Received POST request")
    audio_file = request.files.get('audiofile')
    if not audio_file:
        return jsonify({'error': 'No se proporcionó ningún archivo'}), 400

    try:
        filename = audio_file.filename
        ext = audio_file.filename[-3:]
        s3_client.upload_fileobj(audio_file, S3_BUCKET_NAME, filename)

        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME, 'Key': filename},
                                               ExpiresIn=300)

        job_name = "DEP-call-analytics-job" + str(time.time())

        response = transcribe_client.start_transcription_job(TranscriptionJobName=job_name, Media={
            'MediaFileUri': f's3://{S3_BUCKET_NAME}/{filename}'}, MediaFormat=ext, LanguageCode='es-US', OutputBucketName='my-call-audiotranscriptions-008')
        job_name_trans = response['TranscriptionJob']['TranscriptionJobName']

        while True:
            status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name_trans)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
        if job_status == 'COMPLETED':
            transcription_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(status)
            transcription_text = get_transcription_text(transcription_uri)
            return jsonify({'transcription': transcription_text}), 200
        else:
            return jsonify({'error': 'El trabajo de transcripción falló'}), 500
        return jsonify({'response': status}), 200
    except ClientError as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


def get_transcription_text(transcription_uri: str):
    response = s3_client.get_object(Bucket='my-call-audiotranscriptions-008', Key=transcription_uri.split('/')[-1])
    transcript_data = response['Body'].read()
    transcript_json = json.loads(transcript_data)
    transcript_text = transcript_json['results']['transcripts'][0]['transcript']
    return transcript_text


if __name__ == '__main__':
    app.run()
