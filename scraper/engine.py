from datetime import datetime, timedelta

class WebcrimsBot:
    def __init__(
            self, 
            start_date: datetime | None = None, 
            num_days: int = 7, 
            batch_size: int = 25
        ):
        
        self.start_date = datetime.today() if start_date is None else start_date
        self.end_date = (self.start_date + timedelta(days=num_days))
        self.num_days = num_days
        self.batch_size = batch_size

    def submit_form(self):
        raise NotImplementedError
    
if __name__ == "__main__":
    bot = WebcrimsBot()
    



