import pandas as pd
import os

class DataHandler:
    def __init__(self):
        self.feedback_csv_path = './aritficats/feedback/feedback_data.csv'
        self.feedback_df = pd.DataFrame(columns=['Name','Email','FeedBack' ,'Satisfied'])
        

    def add_feedback(self, name,email, feedback,satisfied):
        new_row = {'Name': name, 'Email' : email ,'FeedBack' : feedback,'Satisfied': satisfied}
        self.feedback_df = pd.concat([self.feedback_df, pd.DataFrame([new_row])], ignore_index=True)
        self.feedback_df.to_csv('./aritficats/feedback/feedback_data.csv', index=False)

    def get_feedback(self): 
        return pd.read_csv(self.feedback_csv_path) if os.path.isfile(self.feedback_csv_path) else pd.DataFrame(columns=['Name','Email','FeedBack', 'Satisfied'])


    def counts_feedback(self):
        df = self.get_feedback()
        avg_feed = df.groupby(['Name', 'Email'])['Satisfied'].mean()
        
        # Filter average satisfaction scores greater than 5
        filter1 = avg_feed[avg_feed > 5]
        filter2 = avg_feed[avg_feed <= 5]
  
        # Count the occurrences of scores greater than 5
        counts1 = filter1.value_counts()
        counts2 = filter2.value_counts()

        # Return the counts
        satisfied = counts1.sum()
        unsatisfied = counts2.sum()
        return satisfied, unsatisfied