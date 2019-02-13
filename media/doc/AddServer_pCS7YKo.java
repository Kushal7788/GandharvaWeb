import java.rmi.*;
import java.rmi.registry.*;
public class AddServer{

	public static void main(String args[]){
	
		try{
			Remote_Interface first_service=new ImplementedRemoteInt();
			
			
			Naming.rebind("rmi://localhost:1904/FirstService",first_service);
			
			
			//first_service object is hosted with name FirstService
		}catch(Exception e){
			System.out.println(e);
		}
	}

}
