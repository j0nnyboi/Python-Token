

function WalletCheck(){
	console.log('1234');
if(!localStorage.getItem('Keypair')) {
	console.log('here');
  populateKeypair();
} else {
	console.log('here1');
  setKeypair();
}
}

function populateKeypair() {
  /*get new key and save client side*/
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "GET",
   url: "WalletNew/",
   data: {},
   success: function callback(response){
               console.log(response);
			   localStorage.setItem('Keypair', response);
            }
});
  
  //save
  console.log('Wallet Saved');

}

function setKeypair() {
  var currentKey = localStorage.getItem('Keypair');/*get client stored keypair*/
  console.log(currentKey)
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
 $.ajax({
	 headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: 'Wallet/',
   data: {'keypair':currentKey},
   success: function callback(response){
               console.log(response);
            }
});
  /*document.getElementById('Keypair').value = currentColor;*/
}

