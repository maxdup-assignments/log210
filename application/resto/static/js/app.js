'use strict';

var app = angular.module('pgApp', []);

app.config(function ($routeProvider) {
  $routeProvider
    .when('/home',
      {
        templateUrl: 'static/partials/home.html'
      })
    .when('/register',
      {
        controller: 'RegisterController',
        templateUrl: 'static/partials/register.html'
      })
    .when('/login',
      {
        controller: 'LoginController',
        templateUrl: 'static/partials/login.html'
      })
    .when('/manage/users',
          {
            controller: 'UserController',
            templateUrl: 'static/partials/manage_users.html'
          })
    .otherwise({ redirectTo: '/home' });
});

app.config(function($httpProvider){
    $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF_TOKEN;
});
