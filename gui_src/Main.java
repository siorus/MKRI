package mkri;
import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {
	
	@Override
	public void start(Stage primaryStage) {
		
		Parent root = null;
		try {
			root = FXMLLoader.load(getClass().getResource("GUI.fxml"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return ;
		}
		Scene scene = new Scene(root);
		primaryStage.setScene(scene);
		primaryStage.setTitle("Hashovací funkce");
		primaryStage.show();
		
		Proces p = new Proces();
		p.setPrimaryStage(primaryStage);

	}

	public static void main(String[] args) {
		launch(args);
	}
}