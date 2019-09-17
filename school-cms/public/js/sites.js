$(function () {
  // main navigation item: active class
  let current = location.pathname;
  $('nav ul li a').each(function () {
    let $this = $(this);
    // if the current path is like this link, make it active
    if (current.startsWith($this.attr('href')) && current.length > 1) {
      $this.addClass('active');
    }
  });
});