__all__ = [
  'OptimizelyError', 'BadRequestError', 'UnauthorizedError', 'ForbiddenError', 'NotFoundError',
  'TooManyRequestsError', 'ServiceUnavailableError', 'InvalidIDError']


class OptimizelyError(Exception):
  """ General exception for all Optimizely Experiments API related issues."""
  pass


class BadRequestError(OptimizelyError):
  """ Exception for when request was not sent in valid JSON."""
  pass


class UnauthorizedError(OptimizelyError):
  """ Exception for when API token is missing or included in the body rather than the header."""
  pass


class ForbiddenError(OptimizelyError):
  """ Exception for when API token is provided but it is invalid or revoked."""
  pass


class NotFoundError(OptimizelyError):
  """ Exception for when the id used in request is inaccurate or token user doesn't have permission to
  view/edit it."""
  pass


class TooManyRequestsError(OptimizelyError):
  """ Exception for when a rate limit for the API is hit."""
  pass


class ServiceUnavailableError(OptimizelyError):
  """ Exception for when the API is overloaded or down for maintenance."""
  pass


class InvalidIDError(OptimizelyError):
  """ Exception for when object is missing its ID."""
  pass