$(function() {
  $('#discover_text_header').click(function() {
    $('#discover_text').fadeToggle(10);
  });

  $('#discover_list_header').click(function() {
    $('#discover_list').fadeToggle(10);
  });

  $('#discover_theory_header').click(function() {
    $('#discover_theory').fadeToggle(10);
  });

  $('#discover_links_header').click(function() {
    $('#discover_links').fadeToggle(10);
  });
});

// function print_attempt(print_try){
// console.log("function started");
//   var print_content=document.getElementById(print_try).innerHTML;
//   var page_content=document.body.innerHTML;
//   document.body.innerHTML=print_content;
//   window.print();
//   document.body.innerHTML=page_content;
// }
