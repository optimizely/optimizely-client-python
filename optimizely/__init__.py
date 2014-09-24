# Optimizely Python bindings
# API docs at http://developers.optimizely.com/
# Authors:
# Andy Harris <andy.harris@optimizely.com>

# configuration variables
api_key = None
api_base = 'https://www.optimizelyapis.com/experiment/v1/'

# Resources
from optimizely.resource import Project, Experiment, Result, Variation, Goal, Audience

# Errors
from optimizely.error import (
    OptimizelyError, BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, TooManyRequestsError,
    ServiceUnavailableError, InvalidIDError)