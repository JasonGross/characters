/*
 * Special event for image load events
 * Needed because some browsers does not trigger the event on cached images.

 * MIT License
 * Paul Irish     | @paul_irish | www.paulirish.com
 * Andree Hansson | @peolanha   | www.andreehansson.se
 * Jason Gross
 * 2011.
 *
 * Usage:
 * $(images).bind('load', function (e) {
 *   // Do stuff on load
 * });
 * 
 * Note that you can bind the 'error' event on data uri images, this will trigger when
 * data uri images isn't supported.
 */
(function ($, src) {
	$.support.cachedImageEventLoad = undefined;
	var doOnNoLoad = []; // because what we don't yet know can still hurt us
	var cached = undefined;
	var oldLoad = $.event.special.load;
	var newLoad = $.event.special.load = {
		add: function (hollaback) {
			if ( this.nodeType === 1 && this.tagName.toLowerCase() === 'img' && this.src !== '' ) {
				var _this = this;
				// If we don't yet "know" whether or not cached images fire load, but we
				// know that the image is cached, then load doesn't fire.
				if ( $.support.cachedImageEventLoad === undefined && cached ) {
					$.support.cachedImageEventLoad = false;
					$.each(doOnNoLoad, function ( fn ) {
						fn();
					});
					doOnNoLoad = null;
				}
				// Image is already complete, fire the hollaback (fixes browser issues were cached
				// images isn't triggering the load event)
				// If we don't yet know whether or not load will automatically fire, push the function
				// onto the list of things to be executed when we figure it out.
				if ( this.complete || this.readyState === 4 ) {
					if ( $.support.cachedImageEventLoad === undefined ) {
						doOnNoLoad.push(function () { hollaback.handler.apply(_this); });
					} else if ( $.support.cachedImageEventLoad === false ) {
						hollaback.handler.apply(this);
					}
				}

				// Check if data URI images is supported, fire 'error' event if not
				else if ( this.readyState === 'uninitialized' && this.src.indexOf('data:') === 0 ) {
					if ( $.support.cachedImageEventLoad === undefined ) {
						doOnNoLoad.push(function () { $(_this).trigger('error'); });
					} else {
						$(this).trigger('error');
					}
				}
			}
		}
	};

	$('<img>')
		.attr('src', src)
		.load(function () {
			$.event.special.load = oldLoad;
			var tempImg = $('<img>')
				.attr('src', src)
				.load(function () {
					$.support.cachedImageEventLoad = true;
					if (cached === false)
						console.warn('jQuery Warning: Cannot determine whether or not load fires on cached images.  Assuming that it does.');
					$(this).remove();
				});
			cached = tempImg.attr('complete') || tempImg.attr('readyState') === 4;
			$.event.special.load = newLoad;
			$(this).remove();
		});
})(jQuery, 'https://jgross.scripts.mit.edu/alphabets/images/down.gif');
