$(document).ready(function () {


  // Contact Form Handler
  var contactForm = $(".contactform")
  var contactFormMethod = contactForm.attr("method")
  var contactFormEndpoint = contactForm.attr("action")


  function displaySubmitting(submitBtn, defaultText, doSubmit) {
    if (doSubmit) {
      submitBtn.addClass("disabled")
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
    } else {
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }

  }


  contactForm.submit(function (event) {
    event.preventDefault()

    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()


    var contactFormData = contactForm.serialize()
    var thisForm = $(this)
    displaySubmitting(contactFormSubmitBtn, "", true)
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function (data) {
        contactForm[0].reset()
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "bootstrap",
        })
        setTimeout(function () {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)
      },
      error: function (error) {
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ""

        $.each(jsonData, function (key, value) { // key, value  array index / object
          msg += key + ": " + value[0].message + "<br/>"
        })

        $.alert({
          title: "Oops!",
          content: msg,
          theme: "bootstrap",
        })

        setTimeout(function () {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)

      }
    })
  })




  // Auto Search
  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']") // input name='q'
  var typingTimer;
  var typingInterval = 500 // .5 seconds
  var searchBtn = searchForm.find("[type='submit']")


  searchInput.keyup(function (event) {
    // key released
    clearTimeout(typingTimer)
    typingTimer = setTimeout(perfomSearch, typingInterval)
  })

  searchInput.keydown(function (event) {
    // key pressed
    clearTimeout(typingTimer)
  })

  function displaySearching() {
    searchBtn.addClass("disabled")
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i>")
  }

  function perfomSearch() {
    displaySearching()
    var query = searchInput.val()
    setTimeout(function () {
      window.location.href = '/search/?q=' + query
    }, 1000)

  }


  // Cart + Add entries 
  var productForm = $(".form-product-ajax") // #form-product-ajax


  productForm.submit(function (event) {
    event.preventDefault();

    //console.log("Form is not sending")
    var thisForm = $(this)

    // var actionEndpoint = thisForm.attr("action"); // API Endpoint
    var actionEndpoint = thisForm.attr("data-endpoint")
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();


    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {

        var quantity = data.equantity
        var cost = data.ecost
        var price = data.pprice
        var slug = data.pslug
        var count = data.ccount
        var one = $("#" + slug)
        var two = $("#" + slug + "r")
        var btnd = $("#" + slug + "d")
        var currentPath = window.location.href

        var status = "Operation Undone";
        if(data.added==1)status = "1 " +  data.ptitle + " has been added to cart";
        else if(data.added==-1)status = "1 " +  data.ptitle + " has been removed from cart";
     
        
        $.alert({
          title: "Cart Updated",
          content: status,
          theme: "bootstrap",
        });
        

        

        one.html(quantity + " x " + price + " €")
        if (currentPath.indexOf("cart") != -1)two.html(cost + " €")
        else two.html( " = " + cost + " €")


        if (quantity > 0) {
          btnd.attr("disabled", false)
        } 
        else {
          btnd.attr("disabled", true)
        }

        var navbarCount = $(".navbar-cart-count")
        navbarCount.text(count)
        

        if (currentPath.indexOf("cart") != -1) {
          refreshTotal()
        }
        
      },
      error: function (errorData) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "bootstrap",
        })
      }
    })

  })


  function refreshTotal() {

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function (data) {


        $(".cart-subtotal").text(data.subtotal)
        $(".cart-total").text(data.total)



      },
      error: function (errorData) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "bootstrap",
        })
      }
    })




  }





})