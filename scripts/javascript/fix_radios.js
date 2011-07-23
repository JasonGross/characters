// from http://evilstreak.co.uk/blog/fixing-change-events-on-radios
(function ($, jQuery, undefined) {
  $.fn.fix_radios = function() {
    function focus() {
      // if this isn't checked then no option is yet selected. bail
      if ( !this.checked ) return;

      // if this wasn't already checked, manually fire a change event
      if ( !this.was_checked ) {
        $( this ).change();
      }
    }

    function change( e ) {
      // shortcut if already checked to stop IE firing again
      if ( this.was_checked ) {
        e.stopImmediatePropagation();
        return;
      }

      // reset all the was_checked properties
      $( "input[name=" + this.name + "]" ).each( function() {
        this.was_checked = this.checked;
      } );
    }

    // attach the handlers and return so chaining works
    return this.focus( focus ).change( change );
  }

  // attach it to all radios on document ready
  $( function() {
    $( "input[type=radio]" ).fix_radios();
  } );

})(jQuery, jQuery);
