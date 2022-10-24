import cv2
from datetime import datetime, timedelta
import pandas as pd

video_path = '/mnt/d/Temp/32440300100L1AC01-1157/session-1653542024-1.mp4'

def get_location_from_timestamp(timestamp):
    for index, row in df.iterrows():
        point_timestamp = int(row['timestamp'])
        if(point_timestamp >= timestamp):
            return row
        # else:
            # print(row['timestamp'])

timestamp_start = 1653542025000
dt_start = datetime.fromtimestamp(timestamp_start / 1000)

timestamp_stop = 1653543379000
dt_stop = datetime.fromtimestamp(timestamp_stop  / 1000)
location_duration = (dt_stop - dt_start).total_seconds() / 60
print('location duration ' + str(location_duration))

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count/fps

print('fps = ' + str(fps))
print('number of frames = ' + str(frame_count))
print('duration (S) = ' + str(duration))
minutes = int(duration/60)
seconds = duration%60
print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
video_last_timestamp = dt_start +  timedelta(seconds=seconds)
print('video last timestamp ' + str(round(video_last_timestamp.timestamp() * 1000)))


df = pd.read_csv('./location.csv')
dt = pd.read_csv('./detect.csv')
detected_lat = []
detected_lng = []

while(cap.isOpened()):
    frame_exists, curr_frame = cap.read()
    if frame_exists:
        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)

        if frame_number > dt.iloc[-1]['frame']:
            break

        frame_timestamps = round(timestamp_start + cap.get(cv2.CAP_PROP_POS_MSEC)) 
        location = get_location_from_timestamp(frame_timestamps)
        result = dt.loc[dt['frame'] == frame_number] 
        if not result.empty:
            print(str(int(frame_number)) + ': ' + str(frame_timestamps) + ' => ' + str(location['latitude']) +',' + str(location['longitude']) + ',' + str(result['class']))
            detected_lat.append(location['latitude'])
            detected_lng.append(location['longitude'])
    else:
        break

cap.release()
do = dt.assign(lat=detected_lat, lng=detected_lng)
do.to_csv('detect_location.csv', encoding='utf-8', index=False)



# timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
# print(timestamps)
# calc_timestamps = [0.0]
# while(cap.isOpened()):
#     frame_exists, curr_frame = cap.read()
#     if frame_exists:
#         # timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
#         # calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
#         timesync = round(time_start + cap.get(cv2.CAP_PROP_POS_MSEC)) 
#         print(timesync)

#     else:
#         break

# cap.release()

# for i, (ts, cts) in enumerate(zip(timestamps, calc_timestamps)):
#     # print('Frame %d difference:'%i, abs(ts - cts))
#     print('Frame %d timestamp:'%i, cts)