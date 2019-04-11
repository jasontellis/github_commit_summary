import requests
import time


class GitCommitSummary:
    """
    Daywise commit summary for given repo over past weeks
    """
    BASE_URL = 'https://api.github.com/repos/{}/stats/commit_activity'
    MIN_WEEKS = 1
    MAX_WEEKS = 52
    MAX_FETCH_RETRIES = 3
    SORT = {'asc': False, 'desc': True}
    DAYS_OF_WEEK = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

    def __init__(self, repo: str, weeks: int = MAX_WEEKS, sort: str = 'desc'):
        """

        :param repo:
        :param weeks:
        :param sort:
        """
        repo = repo.strip()
        self.validate_repo(repo)
        self.validate_weeks(weeks)
        sort = sort.strip().lower()
        self.validate_sort(sort)

        self.url = GitCommitSummary.BASE_URL.format(repo)
        self.sorted_daywise_summary = []
        self.sort = GitCommitSummary.SORT[sort]
        self.weeks = weeks
        self.__set_daywise_summary__()

    @property
    def summary(self) ->list:
        return self.sorted_daywise_summary

    def __set_daywise_summary__(self):

        """
        Summarizes commits in given Github repository for given no. of weeks by each day of week
        :return:
        """
        response = self.fetch_weekwise_commit_statistics()
        response = response[-self.weeks:]
        daywise_avg_commits = {}
        for week in response:
            if 'days' not in week:
                raise ValueError('Unexpected output from Github API. Missing attribute: weeks')
            for day_index, daily_commits in enumerate(week['days']):
                day = GitCommitSummary.DAYS_OF_WEEK[day_index]
                daywise_avg_commits[day] = daywise_avg_commits.get(day, 0) + daily_commits

        # Generate average daily commits over last 'weeks'
        for day in daywise_avg_commits:
            daywise_avg_commits[day] = daywise_avg_commits[day] // self.weeks
        sorted_daywise_commits = sorted(daywise_avg_commits, key=daywise_avg_commits.get, reverse=self.sort)
        self.sorted_daywise_summary = [{'day': day, 'avg_commits': daywise_avg_commits[day]}
                                       for day in sorted_daywise_commits]

    def fetch_weekwise_commit_statistics(self) -> list:
        """
        Fetches commit statistics for repo for past 52 weeks
        :return:
        """
        response = requests.get(self.url)
        if response.status_code != requests.codes.ok and response.status_code != requests.codes.accepted:
            raise response.raise_for_status()

        # If statistics not generated
        fetch_index = 0
        while response.status_code == 202:
            fetch_index += 1
            if fetch_index > GitCommitSummary.MAX_FETCH_RETRIES:
                raise ValueError('Failed to fetch response within {} tries'
                                 .format(GitCommitSummary.MAX_FETCH_RETRIES))
            time.sleep(5)
            response = requests.get(self.url)
        try:
            response = response.json()
        except ValueError as err:
            err.message = 'Invalid json from Github :{}'.format(response)
            raise
        if len(response) != self.MAX_WEEKS:
            raise ValueError('Unexpected output from Github')
        return response

    @staticmethod
    def validate_repo(repo: str):
        """
        Validates repo
        :param repo:
        :return:
        """
        repo_parts = repo.split('/')
        if len(repo_parts) != 2 or not len(repo_parts[0]) or not len(repo_parts[1]):
            raise ValueError('Invalid value for repo.'
                             'Expected: <owner>/<repo>'
                             'Received:{}'.format(repo))

    @staticmethod
    def validate_weeks(weeks: int)-> None:
        """
        Validate the weeks parameter
        :param weeks: No. of weeks up to which commit history is to be considered
        :return:None
        """
        if weeks is None or not GitCommitSummary.MIN_WEEKS <= weeks <= GitCommitSummary.MAX_WEEKS:
            raise ValueError('Illegal value for weeks. '
                             'Expected value between {} and {} both inclusive. '
                             'Received:{}'
                             .format(GitCommitSummary.MIN_WEEKS, GitCommitSummary.MAX_WEEKS, weeks))

    @staticmethod
    def validate_sort(sort: str) ->None:
        """
        Validates sort
        :param sort:
        :return:
        """
        if sort not in GitCommitSummary.SORT:
            raise ValueError('Illegal value for sort. Expected:{}, Received: {}'
                             .format('|'.join(GitCommitSummary.SORT.keys()), sort))

    def __str__(self)-> str:
        """

        :return: String representation of daywise summary
        """
        return '\n'.join(("{:<10s}:\t{}".format(daily_commits['day'], daily_commits['avg_commits'])
                          for daily_commits in self.sorted_daywise_summary))

