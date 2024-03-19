$(function(){
  /**************PRICE RANGE**************** */
  const pricevalue = document.querySelector(".slider-container .price-slider"); 
  const rangePriceInputvalue = document.querySelectorAll(".range-price-input input"); 
  const priceInputvalue = document.querySelectorAll(".price-input input"); 

  // Set the price gap 
  let priceGap = 10;

 // Bind the style from the page loaded
  var minip_price = parseInt(priceInputvalue[0].value); 
  var maxip_price = parseInt(priceInputvalue[1].value); 
  var maxPriceInputStart = rangePriceInputvalue[0].max; 
  pricevalue.style.left = `${(minip_price / maxPriceInputStart) * 100}%`; 
  var maxPriceInputEnd = rangePriceInputvalue[1].max; 
  pricevalue.style.right = `${100 - (maxip_price / maxPriceInputEnd) * 100}%`; 
  rangePriceInputvalue[0].value = minip_price; 
  rangePriceInputvalue[1].value = maxip_price; 

  // Adding event listners to price input elements 

  for (let i = 0; i < priceInputvalue.length; i++) { 
  priceInputvalue[i].addEventListener("input", e => { 

    // Parse min and max values of the range input 
    let minp = parseInt(priceInputvalue[0].value); 
    let maxp = parseInt(priceInputvalue[1].value); 
    let diff = maxp - minp 

    if (minp < 0) { 
      alert("minimum price cannot be less than 0"); 
      priceInputvalue[0].value = 0; 
      minp = 0; 
    } 

    // Validate the input values 
    if (maxp > 500) { 
      alert("maximum price cannot be greater than 500"); 
      priceInputvalue[1].value = 500; 
      maxp = 500; 
    } 

    if (minp > maxp - priceGap) { 
      priceInputvalue[0].value = maxp - priceGap; 
      minp = maxp - priceGap; 

      if (minp < 0) { 
        priceInputvalue[0].value = 0; 
        minp = 0; 
      } 
    } 

    // Check if the price gap is met 
    // and max price is within the range 
    if (diff >= priceGap && maxp <= rangePriceInputvalue[1].max) { 
      if (e.target.className === "min-price-input") { 
        rangePriceInputvalue[0].value = minp; 
        let value1 = rangePriceInputvalue[0].max; 
        pricevalue.style.left = `${(minp / value1) * 100}%`; 
      } 
      else { 
        rangePriceInputvalue[1].value = maxp; 
        let value2 = rangePriceInputvalue[1].max; 
        pricevalue.style.right = 
          `${100 - (maxp / value2) * 100}%`; 
      } 
    } 
  }); 

  // Add event listeners to range input elements 
  for (let i = 0; i < rangePriceInputvalue.length; i++) { 
    rangePriceInputvalue[i].addEventListener("input", e => { 
      let minVal = 
        parseInt(rangePriceInputvalue[0].value); 
      let maxVal = 
        parseInt(rangePriceInputvalue[1].value); 

      let diff = maxVal - minVal 
      
      // Check if the price gap is exceeded 
      if (diff < priceGap) { 
      
        // Check if the input is the min price input 
        if (e.target.className === "min-price") { 
          rangePriceInputvalue[0].value = maxVal - priceGap; 
        } 
        else { 
          rangePriceInputvalue[1].value = minVal + priceGap; 
        } 
      } 
      else { 
      
        // Update price inputs and range progress 
        priceInputvalue[0].value = minVal; 
        priceInputvalue[1].value = maxVal; 
        pricevalue.style.left = 
          `${(minVal / rangePriceInputvalue[0].max) * 100}%`; 
        pricevalue.style.right = 
          `${100 - (maxVal / rangePriceInputvalue[1].max) * 100}%`; 
      } 
    }); 
  } 
  }
  /**************END PRICE RANGE**************** */
  /**************RATE RANGE**************** */
  const ratevalue = document.querySelector(".slider-container .rate-slider"); 
  const rangeRateInputvalue = document.querySelectorAll(".range-rate-input input"); 
  const rateInputvalue = document.querySelectorAll(".rate-input input"); 
  // Set the rate gap 
  let rateGap = 1; 

   // Bind the style from the page loaded
   var minip_rate = parseInt(rateInputvalue[0].value); 
   var maxip_rate = parseInt(rateInputvalue[1].value); 
   var maxRateInputStart = rangeRateInputvalue[0].max; 
   ratevalue.style.left = `${(minip_rate / maxRateInputStart) * 100}%`; 
   var maxRateInputEnd = rangeRateInputvalue[1].max; 
   ratevalue.style.right = `${100 - (maxip_rate / maxRateInputEnd) * 100}%`; 
   rangeRateInputvalue[0].value = minip_rate; 
   rangeRateInputvalue[1].value = maxip_rate; 

  // Adding event listners to rate input elements 
  for (let i = 0; i < rateInputvalue.length; i++) { 
  rateInputvalue[i].addEventListener("input", e => { 

    // Parse min and max values of the range input 
    let minp = parseInt(rateInputvalue[0].value); 
    let maxp = parseInt(rateInputvalue[1].value); 
    let diff = maxp - minp 

    if (minp < 0) { 
      alert("minimum rate cannot be less than 0"); 
      rateInputvalue[0].value = 0; 
      minp = 0; 
    } 

    // Validate the input values 
    if (maxp > 5) { 
      alert("maximum rate cannot be greater than 5"); 
      rateInputvalue[1].value = 5; 
      maxp = 5; 
    } 

    if (minp > maxp - rateGap) { 
      rateInputvalue[0].value = maxp - rateGap; 
      minp = maxp - rateGap; 

      if (minp < 0) { 
        rateInputvalue[0].value = 0; 
        minp = 0; 
      } 
    } 

    // Check if the rate gap is met 
    // and max rate is within the range 
    if (diff >= rateGap && maxp <= rangeRateInputvalue[1].max) { 
      if (e.target.className === "min-rate-input") { 
        rangeRateInputvalue[0].value = minp; 
        let value1 = rangeRateInputvalue[0].max; 
        ratevalue.style.left = `${(minp / value1) * 100}%`; 
      } 
      else { 
        rangeRateInputvalue[1].value = maxp; 
        let value2 = rangeRateInputvalue[1].max; 
        ratevalue.style.right = 
          `${100 - (maxp / value2) * 100}%`; 
      } 
    } 
  }); 

  // Add event listeners to range input elements 
  for (let i = 0; i < rangeRateInputvalue.length; i++) { 
    rangeRateInputvalue[i].addEventListener("input", e => { 
      let minVal = 
        parseInt(rangeRateInputvalue[0].value); 
      let maxVal = 
        parseInt(rangeRateInputvalue[1].value); 

      let diff = maxVal - minVal 
      
      // Check if the rate gap is exceeded 
      if (diff < rateGap) { 
      
        // Check if the input is the min rate input 
        if (e.target.className === "min-rate") { 
          rangeRateInputvalue[0].value = maxVal - rateGap; 
        } 
        else { 
          rangeRateInputvalue[1].value = minVal + rateGap; 
        } 
      } 
      else { 
      
        // Update price inputs and range progress 
        rateInputvalue[0].value = minVal; 
        rateInputvalue[1].value = maxVal; 
        ratevalue.style.left = 
          `${(minVal / rangeRateInputvalue[0].max) * 100}%`; 
        ratevalue.style.right = 
          `${100 - (maxVal / rangeRateInputvalue[1].max) * 100}%`; 
      } 
    }); 
  } 
  }
  /**************END RATE RANGE**************** */
})
