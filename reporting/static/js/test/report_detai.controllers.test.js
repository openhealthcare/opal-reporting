describe('ReportDetailCtrl', function(){
  "use strict";
  var $scope, ctrl, $rootScope, $controller;

  beforeEach(function(){
    module('opal.reporting');
    inject(function($injector){
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $controller  = $injector.get('$controller');
    });

    ctrl = $controller('ReportDetailCtrl', {
        $scope: $scope,
        report: "someReport"
    });
  });

  it('show hoist the report onto scope', function(){
    expect($scope.report).toBe("someReport");
  });
});
