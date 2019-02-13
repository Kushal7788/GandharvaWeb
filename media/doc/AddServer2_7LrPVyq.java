import java.rmi.*;
import java.rmi.registry.*;
public class AddServer2{

	public static void main(String args[]){
	
		try{
			Remote_Interface2 second_service=new ImplementedRemoteInt2();
			
			Naming.rebind("rmi://localhost:1904/SecondService",second_service);
			
			//first_service object is hosted with name FirstService
		}catch(Exception e){
			System.out.println(e);
		}
	}

}
