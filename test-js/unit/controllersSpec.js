'use strict';

var PUBLIC_IDEA_API = '/api/v1/public_ideas/'

describe('Mydeatree controllers', function() {

	describe('PublicIdeaListCtrl', function() {
		var scope, ctrl, $httpBackend;

		beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
			$httpBackend = _$httpBackend_;
			$httpBackend.expectGET(PUBLIC_IDEA_API).respond({
				meta : [],
				objects : [{
					title : 'title 1'
				}, {
					title : 'title 2'
				}]
			});

			scope = $rootScope.$new();
			ctrl = $controller(PublicIdeaListCtrl, {
				$scope : scope
			});

		}));

		it('should create "public_ideas" model with 2 ideas', function() {
			expect(scope.public_ideas).toBeUndefined();
			$httpBackend.flush();

			expect(scope.public_ideas).toEqual([{
				title : 'title 1'
			}, {
				title : 'title 2'
			}]);
		});

	});

	describe('PublicIdeaDetailCtrl', function() {
		var scope, $httpBackend, ctrl;

		beforeEach(inject(function(_$httpBackend_, $rootScope, $routeParams, $controller) {
			$httpBackend = _$httpBackend_;
			$httpBackend.expectGET(PUBLIC_IDEA_API + "999").respond({
				title : 'idea 999'
			});

			$routeParams.ideaId = '999'
			scope = $rootScope.$new();
			ctrl = $controller(PublicIdeaDetailCtrl, {
				$scope : scope
			});
		}));

		it('should fetch public_idea detail', function() {
			expect(scope.public_idea).toBeUndefined();
			$httpBackend.flush();

			expect(scope.public_idea).toEqual({
				title : 'idea 999'
			});
		})
	});
});
