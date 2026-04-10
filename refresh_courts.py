from utils import CourtRefresher

"""
Run to refresh court_codes.json
"""

def refresh_courts():
    cr = CourtRefresher()
    cr.run()
    
if __name__ == "__main__":
    refresh_courts()