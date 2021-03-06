describe('Report', function(){
  "use strict";
  var Report, $window, $httpBackend, $interval, $rootScope;


  beforeEach(function(){
    module('opal.services');
    inject(function($injector){
      Report = $injector.get('Report');
      $window = $injector.get('$window');
      $httpBackend = $injector.get('$httpBackend');
      $rootScope = $injector.get('$rootScope');
    });

    spyOn($window, "open");
  });

  afterEach(function(){
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  var getReport = function(){
    return new Report(
      {create_async_link: "/some_link"},
      {quarter: "2017_1"}
    );
  }

  it('should initialise the report', function(){
    var report = getReport();
    expect(report.create_async_link).toBe("/some_link");
    expect(report.asyncReady).toBe(false);
    expect(report.reportStatusUrl).toBe(null);
    expect(report.reportFileUrl).toBe(null);
    expect(report.criteria).toEqual({quarter: "2017_1"});
  });

  it('should reset the report', function(){
    var report = getReport();
    report.asyncReady = true;
    report.asyncCritera = true;
    report.reportStatusUrl = "blah";
    report.reportFileUrl = "otherBlah";
    report.reset();
    expect(report.asyncReady).toBe(false);
    expect(report.reportStatusUrl).toBe(null);
    expect(report.reportFileUrl).toBe(null);
  });

  it('show open a window on download', function(){
      var report = getReport();
      report.reportFileUrl = "/some_link";
      report.downloadAsynchronously();
      expect($window.open).toHaveBeenCalledWith("/some_link", '_blank');
  });

  it('should trigger $interval on dowload asynchronously', function(){
    var report = getReport();
    $httpBackend.expectPOST('/some_link', {"criteria":"{\"quarter\":\"2017_1\"}"}).respond({
      report_status_url: "/reportStats", report_file_url: "/reportFile"
    });
    report.startAsynchronousTask();
    $httpBackend.flush();
    $rootScope.$apply();
    expect(report.reportStatusUrl).toBe("/reportStats");
    expect(report.reportFileUrl).toBe("/reportFile");
    expect(!!report.interval).toBe(true);
  });

  it('should set async=true when the result comes in', function(){
    var report = new Report({create_async_link: "/some_link"});
    report.reportStatusUrl = "/reportStatus";
    report.asyncCritera = true;
    $httpBackend.expectGET('/reportStatus').respond({
      ready: true
    });
    report.getAsyncStatus();
    $httpBackend.flush();
    $rootScope.$apply();
    expect(report.asyncReady).toBe(true);
  });

});
