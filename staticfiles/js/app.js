var module = angular.module('mydeatree', ['mydeatreeServices'])

module.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
});

module.config(['$routeProvider',
function($routeProvider) {
	$routeProvider.when('/public_ideas/', {
		templateUrl : '/partials/public-ideas-list.html',
		controller : PublicIdeaListCtrl
	}).when('/public_ideas/:ideaId', {
		templateUrl : '/partials/public-idea-detail.html',
		controller : PublicIdeaDetailCtrl
	}).when('/personal_ideas/', {
		templateUrl : '/partials/personal-ideas-list.html',
		controller : PersonalIdeaListCtrl
	}).when('/personal_ideas/:ideaId', {
		templateUrl : '/partials/personal-idea-detail.html',
		controller : PersonalIdeaDetailCtrl
	}).when('/favorite_ideas/', {
		templateUrl : '/partials/favorite-idea-list.html',
		controller : FavoriteIdeaListCtrl
	}).when('/favorite_ideas/:ideaId', {
		templateUrl : '/partials/favorite-idea-detail.html',
		controller : FavoriteIdeaDetailCtrl
	}).otherwise({
		redirectTo : '/public_ideas'
	});
}]);

