
//8uBRV4zUk7ukxxSnnkpm5jqu7hWNSTYgWqPpvf37owMc
//GZfWdsbhYsoSXe3MT2j3mtmmKShe6gjZaYrZ25LAN2kW


var Airbtn = document.getElementById("Airdropbtn");
Airbtn.style.display = "none";
var NFTbtn = document.getElementById("NFTbtn");
NFTbtn.style.display = "none";
var TKbtn = document.getElementById("TKbtn");
TKbtn.style.display = "none";
var Chainbtn = document.getElementById("ChainSelectionbtn");
Chainbtn.style.display = "none";
var Hbtn = document.getElementById("Hombtn");
Hbtn.style.color = '#000000';

function WalletCheck(){
if(!localStorage.getItem('Keypair')) {
	$("#walletpopup").show();
	
} else {
  setKeypair();
  HomePage();
  
}
}


function CreateWallet() {
  /*get new key and save client side*/
  $("#walletpopup").hide();
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "GET",
   url: "WalletNew/",
   data: {},
   success: function callback(response){
               console.log(response);
			   localStorage.setItem('Keypair', response['seed']);
			   //var btn = document.getElementById("WalletBtn");
			   //btn.innerText=response;
			   //document.getElementById("WalletBtn").value=;
			   var btn = document.getElementById("WalletBtn");
					btn.innerText=response['pubkey'];
				BalanceShow()
				var NFTbtn = document.getElementById("NFTbtn");
				var TKbtn = document.getElementById("TKbtn");
				TKbtn.style.display = "block";
			   NFTbtn.style.display = "block";
			   var Chainbtn = document.getElementById("ChainSelectionbtn");
				Chainbtn.style.display = "block";
            }
});
  
  //save
  console.log('Wallet Saved');
 

}

function ImportWallet(){
	$("#walletpopup").hide();
	const val = document.getElementById('importKeypair').value;
	//console.log(val);
	localStorage.setItem('Keypair', val);
}



function setKeypair() {
	var NFTbtn = document.getElementById("NFTbtn");
	var TKbtn = document.getElementById("TKbtn");
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
			   var btn = document.getElementById("WalletBtn");
			   btn.innerText=response;
			   //document.getElementById("WalletBtn").value=response;
			   TKbtn.style.display = "block";
			   NFTbtn.style.display = "block";
			   var Chainbtn = document.getElementById("ChainSelectionbtn");
				Chainbtn.style.display = "block";
			   BalanceShow()
            }
});
  /*document.getElementById('Keypair').value = currentColor;*/
}

function HomePage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "block";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "none";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "none";
	var TokenAcc = document.getElementById("sec-57bf");
    TokenAcc.style.display = "none";
	var TokenEdit = document.getElementById("sec-6518");
    TokenEdit.style.display = "none";
	var NFTbtn = document.getElementById("NFTbtn");
	NFTbtn.style.color = '#000000';
	var TKbtn = document.getElementById("TKbtn");
	TKbtn.style.color = '#000000';
	var Hbtn = document.getElementById("Hbtn");
	Hbtn.style.color = '#6bf2b3';
	
}
function TokenPage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "none";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "block";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "none";
	var TokenAcc = document.getElementById("sec-57bf");
    TokenAcc.style.display = "none";
	var TokenEdit = document.getElementById("sec-6518");
    TokenEdit.style.display = "none";
	var NFTbtn = document.getElementById("NFTbtn");
	NFTbtn.style.color = '#000000';
	var TKbtn = document.getElementById("TKbtn");
	TKbtn.style.color = '#6bf2b3';
	var Hbtn = document.getElementById("Hbtn");
	Hbtn.style.color = '#000000';
	
}
function NFTPage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "none";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "none";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "block";
	var TokenAcc = document.getElementById("sec-57bf");
    TokenAcc.style.display = "none";
	var TokenEdit = document.getElementById("sec-6518");
    TokenEdit.style.display = "none";
	var NFTbtn = document.getElementById("NFTbtn");
	NFTbtn.style.color = '#6bf2b3';
	var TKbtn = document.getElementById("TKbtn");
	TKbtn.style.color = '#000000';
	var Hbtn = document.getElementById("Hbtn");
	Hbtn.style.color = '#000000';
	
}

function TKNAccPage(){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "none";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "none";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "none";
	var TokenAcc = document.getElementById("sec-57bf");
    TokenAcc.style.display = "block";
	var TokenEdit = document.getElementById("sec-6518");
    TokenEdit.style.display = "none";
	
}
function TKNEditPage(Keys){
	var Home = document.getElementById("sec-fb3f");
	Home.style.display = "none";
	var Token = document.getElementById("sec-33e8");
	Token.style.display = "none";
	var NFT = document.getElementById("sec-353e");
	NFT.style.display = "none";
	var TokenAcc = document.getElementById("sec-57bf");
    TokenAcc.style.display = "none";
	var TokenEdit = document.getElementById("sec-6518");
    TokenEdit.style.display = "block";
	document.getElementById("TKNacc").innerHTML = Keys['tokenAcc'];
	document.getElementById("TKNToken").innerHTML = Keys['Token']
	console.log('keys : '+ Keys['Token'] + ' ' + Keys['tokenAcc'])
	
}

var main = document.getElementById('Mainnet');
var test = document.getElementById('Testnet');
var dev = document.getElementById('Devnet');
main.style.color = '#6bf2b3'; 
test.style.color = '#000000';  
dev.style.color = '#000000';  
						
function Chain(chain){
	//console.log("chain change");
	//console.log(chain);
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "ChangeChain/",
   data: {'chain':chain},
   success: function callback(response){
                var main = document.getElementById('Mainnet');
			    var test = document.getElementById('Testnet');
				var dev = document.getElementById('Devnet');
				var Airbtn = document.getElementById("Airdropbtn");

				if(response['endpoint'] == 'Connection Error Mainnet'){
					main.style.color = '#FF0000'; 
					test.style.color = '#000000';  
					dev.style.color = '#000000'; 
					alert(response['endpoint']);
					document.getElementById("walletBalance").innerHTML = 0;
					Airbtn.style.display = "none";
				}else if(response['endpoint'] == 'Connection Error Testnet'){
					main.style.color = '#000000'; 
					test.style.color = '#FF0000';  
					dev.style.color = '#000000';
					alert(response['endpoint']);
					document.getElementById("walletBalance").innerHTML = 0;
					Airbtn.style.display = "none";
				}else if(response['endpoint'] == 'Connection Error Devnet'){
					main.style.color = '#000000'; 
					test.style.color = '#000000';  
					dev.style.color = '#FF0000';
					alert(response['endpoint']);
					document.getElementById("walletBalance").innerHTML = 0;
					Airbtn.style.display = "none";
				
				}else{
					console.log(response['endpoint']);
					BalanceShow()
					if(chain == 'Mainnet'){
						main.style.color = '#6bf2b3'; 
						test.style.color = '#000000';  
						dev.style.color = '#000000';  
						Airbtn.style.display = "none";						
					}else if (chain == 'Testnet'){
						main.style.color = '#000000'; 
						test.style.color = '#6bf2b3';  
						dev.style.color = '#000000';
						Airbtn.style.display = "block";
				}else if (chain == 'Devnet'){
						main.style.color = '#000000'; 
						test.style.color = '#000000';  
						dev.style.color = '#6bf2b3';
						Airbtn.style.display = "block";
				}
            }
   }
});
	
	
}

function BalanceShow(){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "Balance/",
   data: {},
   success: function callback(response){
	   var balstr = (response['bal'] + ' Safe  ' + '$' + response['BWorth'])
	   document.getElementById("walletBalance").innerHTML = balstr;
	
   }
});
}

function Airdrop(){
	
	var Loading = document.getElementById('loadingSpin');
	Loading.style.display = "block";
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "Airdrop/",
   data: {},
   success: function callback(response){
	   console.log(response)
	   
	   Loading.style.display = "none";
	   
	  //alert('Airdrop tx : ' + response);
	  BalanceShow()
   }
});
}


function NewToken() {
  /*get new key and save client side*/
  var Loading = document.getElementById('loadingSpin');
	Loading.style.display = "block";
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "GET",
   url: "NewToken/",
   data: {},
   success: function callback(response){
               console.log(response);
			   Loading.style.display = "none";
			   alert('Token PubKey : ' + response);
			   TKNAccPage()
			   //var btn = document.getElementById("WalletBtn");
			   //btn.innerText=response;
			   //document.getElementById("WalletBtn").value=;
            }
});
}

function LoadTokenKey(){
	const TokenPubkey = document.getElementById('TokenLoadStr').value;
	//console.log(val);
	var Loading = document.getElementById('loadingSpin');
	Loading.style.display = "block";
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "loadToken/",
   data: {'Token':TokenPubkey},
   success: function callback(response){
		Loading.style.display = "none";
		console.log(response);
		TKNAccPage()
   }
});
}

function NewTokenACC() {
  /*get new key and save client side*/
  var Loading = document.getElementById('loadingSpin');
	Loading.style.display = "block";
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "GET",
   url: "NewTokenAcc/",
   data: {},
   success: function callback(response){
               console.log(response);
			   Loading.style.display = "none";
			   alert('Token Account PubKey : ' + response['tokenAcc']);
				TKNEditPage(response)
			   //var btn = document.getElementById("WalletBtn");
			   //btn.innerText=response;
			   //document.getElementById("WalletBtn").value=;
            }
});
}

function LoadTokenACC(){
	const TokenPubkey = document.getElementById('TokenACCLoadStr').value;
	//console.log(val);
	var Loading = document.getElementById('loadingSpin');
	Loading.style.display = "block";
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "loadTokenAcc/",
   data: {'Token':TokenPubkey},
   success: function callback(response){
		console.log(response['tokenAcc']);
		Loading.style.display = "none";
		TKNEditPage(response);
		BalanceShow();		
		TKNBal();
   }
});
}
//GRcXwocyawfcpZ1Ff3nY3VycrzvpcRJyVa2WBPfXpbyh
//CXyvCTvfrgYdYNVqApeW4taPtDxp1LNQDktZXfRhr2vr
function TKNBal(){
	//console.log(val);
	var Loading = document.getElementById('loadingSpin');
	Loading.style.display = "block";
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "TKNBal/",
   data: {},
   success: function callback(response){
		Loading.style.display = "none";
		console.log(response);
		document.getElementById("TKNBall").innerHTML = response['TKbal'];
   }
});
}

function TKMint(){
	//console.log(val);
	const TKNamount = document.getElementById('MintAmmt').value;
	var Loading = document.getElementById('lo1adingSpin');
	Loading.style.display = "block";
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "TKMint/",
   data: {'amaount':TKNamount},
   success: function callback(response){
		Loading.style.display = "none";
		console.log(response);
		BalanceShow();
		TKNBal();
   }
});
}


function Tokenreg(){
	//console.log(val);
	
	var Loading = document.getElementById('loadingSpin');
	//Loading.style.display = "block";
	 const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	 
	 var Name = document.getElementById('TR_Name').value;
	var Sym = document.getElementById('TR_Sym').value;
	var Des = document.getElementById('TR_Des').value;
	console.log(Name);
	console.log(Sym);
	console.log(Des);
	
	var File = document.getElementById('file').file;
	
  $.ajax({
	  headers: {'X-CSRFToken': csrftoken},
   type: "POST",
   url: "TokenReg/",
   data: {"name": Name,"Symble": Sym,"message": Des, 'File':File},
   success: function callback(response){
		Loading.style.display = "none";
		console.log(response);
   }
});
}
