import unittest
import requests
from GitCommitSummary import GitCommitSummary


class TestGitCommitSummary(unittest.TestCase):

    def test_validate_repo(self):
        with self.assertRaises(ValueError):
            GitCommitSummary.validate_repo('kubernetes kubernetes')
            GitCommitSummary.validate_repo('kubernetes/')
            GitCommitSummary.validate_repo('/kubernetes')
            GitCommitSummary.validate_repo('')
            GitCommitSummary.validate_repo(None)
        GitCommitSummary.validate_repo('kubernetes/kubernetes')
        GitCommitSummary.validate_repo('  kubernetes/kubernetes')
        GitCommitSummary.validate_repo('kubernetes/kubernetes  ')
        GitCommitSummary.validate_repo('  kubernetes/kubernetes  ')

    def test_validate_weeks(self):
        with self.assertRaises(ValueError):
            GitCommitSummary.validate_weeks(None)
            GitCommitSummary.validate_weeks('1')
            GitCommitSummary.validate_weeks(GitCommitSummary.MIN_WEEKS - 1)
            GitCommitSummary.validate_weeks(0)
            GitCommitSummary.validate_weeks(GitCommitSummary.MAX_WEEKS + 1)
        GitCommitSummary.validate_weeks(1)
        GitCommitSummary.validate_weeks(2)
        GitCommitSummary.validate_weeks(52)
        GitCommitSummary.validate_weeks(26)

    def test_validate_sort(self):
        with self.assertRaises(ValueError):
            GitCommitSummary.validate_sort(None)
            GitCommitSummary.validate_sort('')
            GitCommitSummary.validate_sort(1)
            GitCommitSummary.validate_sort(-1)
            GitCommitSummary.validate_sort('ascending')
            GitCommitSummary.validate_sort('descending')
            GitCommitSummary.validate_sort('ASC')
            GitCommitSummary.validate_sort('DESC')
        GitCommitSummary.validate_sort('asc')
        GitCommitSummary.validate_sort('desc')

    def test_git_commit_summary(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            GitCommitSummary('kubernates/kubernates')

        with self.assertRaises(ValueError):
            GitCommitSummary('kubernetes/kubernetes')
            GitCommitSummary('kubernetes/kubernetes', weeks=60, sort='desc')
            GitCommitSummary('kubernetes/kubernetes', weeks=0, sort='asc')
            GitCommitSummary('kubernetes/kubernetes', sort='de3sc')
            GitCommitSummary('kubernetes/kubernetes', sort='aesc')
            GitCommitSummary('kubernetes/kubernetes', weeks=53)
            GitCommitSummary('kubernetes/kubernetes', weeks=-1)

        GitCommitSummary('kubernetes/kubernetes')
        desc = (GitCommitSummary('kubernetes/kubernetes', weeks=20, sort='desc')).summary
        desc.sort(key=lambda x: x['avg_commits'], reverse=False)
        asc = GitCommitSummary('kubernetes/kubernetes', weeks=20, sort='asc').summary
        self.assertEqual(desc, asc, 'Descending Summary matches Ascending Summary in reverse')

        GitCommitSummary('kubernetes/kubernetes', sort='desc')
        GitCommitSummary('kubernetes/kubernetes', sort='asc')
        GitCommitSummary('kubernetes/kubernetes', weeks=30)
        GitCommitSummary('kubernetes/kubernetes', weeks=40)


