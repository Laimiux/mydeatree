'use strict';

angular.module('mydeatreeServices', ['ngResource']).factory('PublicIdea', function($resource) {
	return $resource(PUBLIC_IDEA_API + ':ideaId', {}, {
		query : { method: 'GET', params: {ideaId : 'public_ideas'}, isArray: true}
	});
});

/*
 *   return $resource('phones/:phoneId.json', {}, {
    query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
  });
 */
