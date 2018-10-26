describe('ReportDetailCtrl', function(){
  "use strict";
  var $scope, ctrl, $rootScope, $controller, $httpBackend;
  var Report, report, criteria, criteriaJson, reportDefinition;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $controller  = $injector.get('$controller');
      $httpBackend  = $injector.get('$httpBackend');
    });

    report = jasmine.createSpyObj(["startAsynchronousTask"])
    Report = jasmine.createSpy("Report");
    Report.and.returnValue(report);
    reportDefinition = "someReport"

    ctrl = $controller('ReportDetailCtrl', {
        $scope: $scope,
        reportDefinition: reportDefinition,
        Report: Report
    });

    criteria = {some: "criteria"}
    $scope.startDownload(criteria);
    criteriaJson = JSON.stringify(criteria);

  });

  afterEach(function(){
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should create a report on start download', function(){
    expect(Report).toHaveBeenCalledWith(reportDefinition, criteria);
    expect(report.startAsynchronousTask).toHaveBeenCalled();
  });

  it('show hoist the report onto scope', function(){
    expect($scope.reports[criteriaJson]).toBe(report);
  });
});
