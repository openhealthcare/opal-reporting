angular.module('opal.reporting').controller(
    'ReportDetailCtrl', function($scope, report){
      $scope.report = report;
      // To keep params out of URLs we're using a form-like
      // POST request and serialising things with the value of
      // a hidden field being a JSON version of the criteria variable
      $scope.JSON = window.JSON;
    }
);
