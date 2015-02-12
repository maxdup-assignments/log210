angular.module('restoApp', ['resto.userControllers', 'resto.restoControllers', 'resto.services'])
.config(($routeProvider, $httpProvider) ->
  $routeProvider
  .when '/home',
    templateUrl: 'static/partials/home.html'
  .when '/register',
    controller: 'UserController',
    templateUrl: 'static/partials/register.html'
  .when '/profile',
    controller: 'UserController',
    templateUrl: 'static/partials/profile.html'
  .when '/admin/users',
    controller: 'UserController',
    templateUrl: 'static/partials/admin_users.html'
  .when '/admin/resto',
    controller: 'RestaurantController',
    templateUrl: 'static/partials/admin_resto.html'
  .when '/manage_menu/:param',
    controller: 'RestaurantController',
    templateUrl: 'static/partials/manage_menu.html'

  .otherwise
    redirectTo: '/home'

  $httpProvider.defaults.headers.common['X-CSRFToken'] = CSRF_TOKEN
)
