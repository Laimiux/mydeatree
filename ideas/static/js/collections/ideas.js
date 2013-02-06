var app = app || {}; ( function() {
		var IdeaList = Backbone.Collection.extend({
			url : function() {
				return this.next || IDEA_API	
			},			
			model : app.Idea,
			parse : function(data) {
				this.next = data.meta.next;
				if(this.next == null) {
					this.completedSync = true;
				}
				return data.objects;
			},
		});

		// Create our global collection of **Ideas**.
		app.Ideas = new IdeaList();
	}());
