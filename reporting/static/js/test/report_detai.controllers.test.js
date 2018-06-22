describe('ReportDetailCtrl', function(){
  "use strict";
  var $scope, ctrl, $rootScope, $controller, $httpBackend;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $controller  = $injector.get('$controller');
      $httpBackend  = $injector.get('$httpBackend');
    });

    ctrl = $controller('ReportDetailCtrl', {
        $scope: $scope,
        report: "someReport"
    });
  });

  afterEach(function(){
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('show hoist the report onto scope', function(){
    expect($scope.report).toBe("someReport");
  });
});
