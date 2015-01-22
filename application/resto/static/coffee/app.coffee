angular.module('restoApp', ['resto.controllers','resto.services'])
.config(($routeProvider, $httpProvider) ->
  $routeProvider
  .when '/home',
    templateUrl: 'static/partials/home.html'
  .when '/register',
    controller: 'RegisterController',
    templateUrl: 'static/partials/register.html'
  .when '/manage/users',
    controller: 'UserController',
    templateUrl: 'static/partials/manage_users.html'
  .otherwise
    redirectTo: '/home'
  $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF_TOKEN
)
