class UnknownError(Exception):
  def __init__(self, message, code: int, errors = None):
    msg = f"{message}, code: {code}"
    if errors is not None:
      msg += f", errors: {errors}"

    super().__init__(msg)
    self.code = code
    self.errors = errors

class RateError(UnknownError):
  def __init__(self, time: float):
    super().__init__(f"The resource is being rate limited for {time} secs.", -1)
    self.time = time