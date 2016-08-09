import toastutil
from datetime import date

if __name__ == "__main__":
  victim = toastutil.prompt_for_member()
  asof = str(date.today())
  num_speeches = toastutil.num_of(victim, 'speaker', asof, False)
  num_evals = toastutil.num_of(victim, 'eval', asof, False) 
  print "{} speeches, {} evaluations for member {}".format( \
        num_speeches, num_evals, victim)
