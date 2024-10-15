import pandas as pd 
from logger import app_logger
from datetime import datetime, timedelta
from flask import jsonify
from stream_insight import DB

class DataVisualization:
    
    def __init__(self):
        self.database=DB()
    def fetch_data(self, object_class, hours_in_past):
        try:
            df = self.database.query_objects_by_class(object_class)
            
            df['first_detected_time'] = pd.to_datetime(df['first_detected_time'])

            if df['first_detected_time'].dt.tz is None:
                df['first_detected_time'] = df['first_detected_time'].dt.tz_localize('UTC')
            else:
                df['first_detected_time'] = df['first_detected_time'].dt.tz_convert('UTC')

            time_threshold = pd.Timestamp.now(tz='UTC') - pd.Timedelta(hours=hours_in_past)
            
            df = df[df['first_detected_time'] >= time_threshold]

            df = df.sort_values('first_detected_time')

            df['affluence'] = df.index + 1  # Cumulative count of rows up to each timestamp

            # Return the filtered and sorted DataFrame
            return df
        except Exception as e:
            app_logger.error(f"Error fetching data from database: {str(e)}")
            raise
    def cumulative_affluence_json(self, df):
        """
        Generate JSON data for cumulative affluence over time.
        Input: DataFrame created by fetch_data method.
        Output: JSON structure for cumulative affluence chart.
        """
        data = {
            'timestamps': df['first_detected_time'].astype(str).tolist(),  
            'affluence': df['affluence'].tolist(),  
        }
        return jsonify(data)

    def instantaneous_affluence_json(self, df, interval='15T'):
        """
        Generate JSON data for instantaneous affluence (counts per time interval).
        Input: DataFrame created by fetch_data method.
        Output: JSON structure for instantaneous affluence chart.
        """
        df.set_index('first_detected_time', inplace=True)
        resampled_df = df.groupby(pd.Grouper(freq=interval)).size().reset_index(name='count')

        data = {
            'timestamps': resampled_df['first_detected_time'].astype(str).tolist(),  # Convert timestamps to strings
            'counts': resampled_df['count'].tolist(),  
        }
        return jsonify(data)