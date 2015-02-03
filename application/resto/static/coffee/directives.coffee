angular.module('resto.directives', [])
.directive('ngMenueditor', () ->
  {
    restrict: 'E',
    scope: false,
    templateUrl: '/static/partials/widgets/menu.html'
  }
)