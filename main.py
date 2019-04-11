from argparse import ArgumentParser
from GitCommitSummary import GitCommitSummary

parser = ArgumentParser(description='Daywise Github Repository Commits')
parser.add_argument('repo',  help='Repository in the form: <owner>/<repo> e.g. kubernetes/kubernetes')
parser.add_argument('--sort', metavar='sort', help='Sort order: asc or desc. \nDefault: desc', default='desc')
parser.add_argument('--weeks', metavar='weeks', help="No.of weeks for which to "
                                                     "summarize commits. Integer between 1 and 52 both inclusive."
                                                     "\nDefault: {}".format(GitCommitSummary.MAX_WEEKS),
                    default=GitCommitSummary.MAX_WEEKS,
                    type=int)
args = parser.parse_args()
print(GitCommitSummary(repo=args.repo, weeks=args.weeks, sort=args.sort))




