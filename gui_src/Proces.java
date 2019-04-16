package mkri;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ResourceBundle;

import com.sun.xml.internal.ws.policy.privateutil.PolicyUtils.Text;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;

import javafx.stage.FileChooser;
import javafx.stage.FileChooser.ExtensionFilter;
import javafx.stage.Stage;

public class Proces implements Initializable {

	@FXML
	private Button button;

	@FXML
	private Button TXTbutton;

	@FXML
	private Button BINbutton;
	
	@FXML
	private Button Vymazatbutton;

	@FXML
	private TextField hashVstupniPole;
	
	@FXML
	private TextField hashVstupniPole2;

	@FXML
	private TextField hashImplementace;

	@FXML
	private TextField hashKnihovna;
	
	@FXML
	private TextField hashPomociKnihovnySHA1;
	
	@FXML
	private TextField hashPomociKnihovnySHA2;
	
	@FXML
	private TextField hashPomociKnihovnySHA3;
	
	@FXML
	private TextField hashPomociKnihovnyBLAKE2;

	@FXML
	private TextField hashPorovnani;
	
	@FXML
	private TextField bitDelkaMD5_python;
	
	@FXML
	private TextField bitDelkaMD5_lib;
	
	@FXML
	private TextField bitDelkaSHA1;
	
	@FXML
	private TextField bitDelkaSHA2;
	
	@FXML
	private TextField bitDelkaSHA3;
	
	@FXML
	private TextField bitDelkaBLAKE2;

	private String ziskanyHash = "";

	private String ziskanyHashZKnihovny = "";

	public static Stage primaryStage;
	
	private boolean windowsOS=true;
	
	@FXML
	private TextField zadanaCestaTXT;
	
	@FXML
	private TextField zadanaCestaBin;
	
	@FXML
	private TextField zadanaCestaTXT2;
	
	@FXML
	private TextField zadanaCestaBin2;

	@FXML
	public void HashTEXT(ActionEvent event) {
		
		
		String zadanyText = hashVstupniPole.getText();
		zadanyText = '"' + zadanyText + '"';
		
		if (zadanyText.length() == 0)
			return;
		
		detekujOS();

		// SKRIPT IMPLEMENTACE mkrihash.py
		this.ziskanyHash = hashFunkce("mkrihash.py", "-i", zadanyText);

		// nastav Vystup
		hashImplementace.setText(ziskanyHash);
		bitDelkaMD5_python.setText(""+ziskanyHash.length()+ " z, " + ziskanyHash.length()*4 + " b");

		// SKRIPT KNIHOVNA mkrihash_lib.py
		pouzijKnihovnuMD5("-a", "md5", "-i", zadanyText);

		// Porovnani HASHU
		porovnejHashe();
	}

	String cestaKsouboruTXT = "";
	String cestaKsouboruBIN = "";

	@FXML
	public void HashTXTFile_nacti_cestu(ActionEvent event)
	{
		detekujOS();
		
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Zdrojový soubor");
		//fileChooser.getExtensionFilters().addAll(new ExtensionFilter("Text Files", "*.txt", "*.bin"));

		File soubor = fileChooser.showOpenDialog(primaryStage);
		if (soubor != null) {
			// primaryStage.display(soubor);
		}

		// System.out.println(soubor.getAbsolutePath());

		// cesta k nactenemu souboru
		cestaKsouboruTXT = soubor.getPath();
		//cestaKsouboruTXT = '"' + cestaKsouboruTXT + '"';
		
		zadanaCestaTXT.setText(cestaKsouboruTXT);
		cestaKsouboruTXT = '"' + cestaKsouboruTXT + '"';
	}
	
	
	public void HashTXTFile() {
		
		if(cestaKsouboruTXT.length()==0)return;
		
		// SKRIPT IMPLEMENTACE mkrihash.py
		this.ziskanyHash = hashFunkce("mkrihash.py", "-t", cestaKsouboruTXT);

		// nastav Vystup
		hashImplementace.setText(ziskanyHash);
		bitDelkaMD5_python.setText(""+ziskanyHash.length()+ " z, " + ziskanyHash.length()*4 + " b");

		// SKRIPT KNIHOVNA mkrihash_lib.py
		pouzijKnihovnuMD5("-a", "md5", "-t", cestaKsouboruTXT);

		// Porovnani HASHU
		porovnejHashe();

	}
	
	@FXML
	public void HashBINFile_nacti_cestu(ActionEvent event)
	{
		detekujOS();
		
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Zdrojový soubor");
		//fileChooser.getExtensionFilters().addAll(new ExtensionFilter("Text Files", "*.txt", "*.bin"));

		File soubor = fileChooser.showOpenDialog(primaryStage);
		if (soubor != null) {
			// primaryStage.display(soubor);
		}

		// System.out.println(soubor.getAbsolutePath());

		// cesta k nactenemu souboru
		cestaKsouboruBIN = soubor.getPath();
		
		zadanaCestaBin.setText(cestaKsouboruBIN);
		cestaKsouboruBIN = '"' + cestaKsouboruBIN + '"';
		
	}

	
	public void HashBINFile() {
		
		
		if(cestaKsouboruBIN.length()==0)return;

		// SKRIPT IMPLEMENTACE mkrihash.py
		this.ziskanyHash = hashFunkce("mkrihash.py", "-b", cestaKsouboruBIN);

		// nastav Vystup
		hashImplementace.setText(ziskanyHash);
		bitDelkaMD5_python.setText(""+ziskanyHash.length()+ " z, " + ziskanyHash.length()*4 + " b");

		// SKRIPT KNIHOVNA mkrihash_lib.py
		pouzijKnihovnuMD5("-a", "md5", "-b", cestaKsouboruBIN);

		// Porovnani HASHU
		porovnejHashe();
	}
	
	@FXML
	public void Vymazat(ActionEvent event) {
		
		this.ziskanyHash = "";
		this.ziskanyHashZKnihovny = "";
		
		hashPorovnani.setStyle("-fx-text-inner-color: black;");
		hashPorovnani.setText("SHODA?");
		
		hashImplementace.setText("");
		hashKnihovna.setText("");
		
		zadanaCestaTXT.setText("");
		zadanaCestaBin.setText("");
		
		hashVstupniPole.setText("");
		
		bitDelkaMD5_python.setText("");
		bitDelkaMD5_lib.setText("");
	}

	public void porovnejHashe() {

		if (ziskanyHash.compareTo(ziskanyHashZKnihovny) == 0) {

			hashPorovnani.setStyle("-fx-text-inner-color: green;");
			hashPorovnani.setText("SHODA");
		} else {

			hashPorovnani.setStyle("-fx-text-inner-color: red;");
			hashPorovnani.setText("CHYBA!");
		}
	}

	public void pouzijKnihovnuMD5(String parametr1, String zadanyText1, String parametr2, String zadanyText2) {
		String hash = hashLibFunkce("mkrihash_lib.py", parametr1, zadanyText1, parametr2, zadanyText2);
		
		hashKnihovna.setText(hash);
		bitDelkaMD5_lib.setText(""+ziskanyHash.length()+ " z, " + ziskanyHash.length()*4 + " b");

		ziskanyHashZKnihovny = hash;
	}

	public String hashFunkce(String nazevSouboru, String parametr, String zadanyText) {
		String vloz = nazevSouboru + " " + parametr + " " + zadanyText; // napriklad "mkrihash.py -i aaa"
		String hash = "";
		ProcessBuilder processBuilder = new ProcessBuilder();

		if(this.windowsOS)processBuilder.command("cmd.exe", "/c", vloz);
		else processBuilder.command("/bin/bash", "/c", vloz);

		try {

			Process proces = processBuilder.start();

			BufferedReader reader = new BufferedReader(new InputStreamReader(proces.getInputStream()));

			String radek;

			while ((radek = reader.readLine()) != null) {
				// System.out.println(radek);
				hash = radek;
			}

			hash = hash.substring(10, hash.length());
			// System.out.println(hash);

			int exitCode = proces.waitFor();
			// System.out.println("\nExited with error code : " + exitCode);

		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		return hash;
	}
	
	// pro knihovnu
	public String hashLibFunkce(String nazevSouboru, String parametr1, String zadanyText1, String parametr2, String zadanyText2) {
		String vloz = nazevSouboru + " " + parametr1 + " " + zadanyText1 + " " + parametr2 + " " + zadanyText2; // napriklad "mkrihash.py -i aaa"
		//vloz = "mkrihash_lib.py -i a -a "+ '"' + "md5"+ '"'; 
		String hash = "";
		ProcessBuilder processBuilder2 = new ProcessBuilder();

		if(this.windowsOS)processBuilder2.command("cmd.exe", "/c", vloz);
		else processBuilder2.command("/bin/bash", "/c", vloz);

		try {

			Process proces = processBuilder2.start();

			BufferedReader reader = new BufferedReader(new InputStreamReader(proces.getInputStream()));

			String radek;

			while ((radek = reader.readLine()) != null) {
				// System.out.println(radek);
				hash = radek;
			}

			hash = hash.substring(10, hash.length());
			//System.out.println(hash);

			int exitCode = proces.waitFor();
			// System.out.println("\nExited with error code : " + exitCode);

		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		return hash;
	}
	
	public void detekujOS()
	{
		String jmeno = System.getProperty("os.name");
		jmeno = jmeno.toLowerCase();
		//System.out.println(jmeno);
		if(jmeno.contains("windows"))this.windowsOS=true;
		else this.windowsOS = false;
			
	}

	public static Stage getPrimaryStage() {
		return primaryStage;
	}

	public static void setPrimaryStage(Stage primaryStage) {
		Proces.primaryStage = primaryStage;
	}

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		// TODO Auto-generated method stub
	}
	
	// ----------------------------- DALSI ALGORITMY --------------------
	String cestaTXT2;
	
	//aby jsme vedeli, co posledniho bylo aktivni
	boolean TXTactive=false;
	boolean BINactive=false;
	boolean TEXTactive=true;
	
	@FXML
	public void nastavCestuTXT2(ActionEvent event) {
	TXTactive=true;
	BINactive=false;
	TEXTactive=false;
	
		detekujOS();
		
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Zdrojový soubor");
		//fileChooser.getExtensionFilters().addAll(new ExtensionFilter("Text Files", "*.txt", "*.bin"));

		File soubor = fileChooser.showOpenDialog(primaryStage);
		if (soubor != null) {
			// primaryStage.display(soubor);
		}

		// System.out.println(soubor.getAbsolutePath());

		// cesta k nactenemu souboru
		cestaTXT2 = soubor.getPath();
		
		zadanaCestaTXT2.setText(cestaTXT2);
		cestaTXT2 = '"' + cestaTXT2 + '"';

	}
	
	String cestaBIN2;
	
	@FXML
	public void nastavCestuBIN2(ActionEvent event) {
		TXTactive=false;
		BINactive=true;
		TEXTactive=false;
		detekujOS();
		
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Zdrojový soubor");
		//fileChooser.getExtensionFilters().addAll(new ExtensionFilter("Text Files", "*.txt", "*.bin"));

		File soubor = fileChooser.showOpenDialog(primaryStage);
		if (soubor != null) {
			// primaryStage.display(soubor);
		}

		// System.out.println(soubor.getAbsolutePath());

		// cesta k nactenemu souboru
		cestaBIN2 = soubor.getPath();
		
		zadanaCestaBin2.setText(cestaBIN2);
		cestaBIN2 = '"' + cestaBIN2 + '"';

	}
	
	
	@FXML
	public void SHA1(ActionEvent event) {
	
		String zadanyText = hashVstupniPole2.getText();

		
			if(TXTactive)
			{
				String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha1", "-t", cestaTXT2);
				hash = hash.substring(1, hash.length());
				hashPomociKnihovnySHA1.setText(hash);
				bitDelkaSHA1.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
				
			}
			else 
				if(BINactive)
				{
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha1", "-b", cestaBIN2);
					hash = hash.substring(1, hash.length());
					hashPomociKnihovnySHA1.setText(hash);
					bitDelkaSHA1.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
				}
				else 
					if(TEXTactive)
					{
					if(zadanyText.length()==0)return;	
					zadanyText = '"' + zadanyText + '"';
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha1", "-i", zadanyText);
					hash = hash.substring(1, hash.length());
					hashPomociKnihovnySHA1.setText(hash);
					bitDelkaSHA1.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
					}
			
		
	}
	
	@FXML
	public void SHA2(ActionEvent event) {
	
		String zadanyText = hashVstupniPole2.getText();

		
			if(TXTactive)
			{
				String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha2", "-t", cestaTXT2);
				hash = hash.substring(1, hash.length());
				hashPomociKnihovnySHA2.setText(hash);
				bitDelkaSHA2.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
			}
			else 
				if(BINactive)
				{
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha2", "-b", cestaBIN2);
					hash = hash.substring(1, hash.length());
					hashPomociKnihovnySHA2.setText(hash);
					bitDelkaSHA2.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
				}
				else 
					if(TEXTactive)
					{
					if(zadanyText.length()==0)return;
					zadanyText = '"' + zadanyText + '"';
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha2", "-i", zadanyText);
					hash = hash.substring(1, hash.length());
					hashPomociKnihovnySHA2.setText(hash);
					bitDelkaSHA2.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
					}
			
		
	}
	
	@FXML
	public void SHA3(ActionEvent event) {
	
		String zadanyText = hashVstupniPole2.getText();

		
			if(TXTactive)
			{
				String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha3", "-t", cestaTXT2);
				hash = hash.substring(1, hash.length());
				hashPomociKnihovnySHA3.setText(hash);
				bitDelkaSHA3.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
			}
			else 
				if(BINactive)
				{
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha3", "-b", cestaBIN2);
					hash = hash.substring(1, hash.length());
					hashPomociKnihovnySHA3.setText(hash);
					bitDelkaSHA3.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
				}
				else 
					if(TEXTactive)
					{
					if(zadanyText.length()==0)return;
					zadanyText = '"' + zadanyText + '"';
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "sha3", "-i", zadanyText);
					hash = hash.substring(1, hash.length());
					hashPomociKnihovnySHA3.setText(hash);
					bitDelkaSHA3.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
					}
			
		
	}
	
	@FXML
	public void BLAKE2(ActionEvent event) {
	
		String zadanyText = hashVstupniPole2.getText();

		
			if(TXTactive)
			{
				String hash = hashLibFunkce("mkrihash_lib.py","-a", "blake2", "-t", cestaTXT2);
				hash = hash.substring(3, hash.length());
				hashPomociKnihovnyBLAKE2.setText(hash);
				bitDelkaBLAKE2.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
			}
			else 
				if(BINactive)
				{
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "blake2", "-b", cestaBIN2);
					hash = hash.substring(3, hash.length());
					hashPomociKnihovnyBLAKE2.setText(hash);
					bitDelkaBLAKE2.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
				}
				else 
					if(TEXTactive)
					{
					if(zadanyText.length()==0)return;
					zadanyText = '"' + zadanyText + '"';
					String hash = hashLibFunkce("mkrihash_lib.py","-a", "blake2", "-i", zadanyText);
					hash = hash.substring(3, hash.length());
					hashPomociKnihovnyBLAKE2.setText(hash);
					bitDelkaBLAKE2.setText(""+hash.length()+ " z, " + hash.length()*4 + " b");
					}
		
	}
	
	public void vymazDruhouCast()
	{
		hashPomociKnihovnySHA1.setText("");
		hashPomociKnihovnySHA2.setText("");
		hashPomociKnihovnySHA3.setText("");
		hashPomociKnihovnyBLAKE2.setText("");
		
		hashVstupniPole2.setText("");
		zadanaCestaTXT2.setText("");
		zadanaCestaBin2.setText("");
		
		bitDelkaSHA1.setText("");
		bitDelkaSHA2.setText("");
		bitDelkaSHA3.setText("");
		bitDelkaBLAKE2.setText("");
	}
	
	

}
