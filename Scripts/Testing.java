/*UNIT TESTING FOR USER INTERFACE, JUNIT TESTING WITHIN THE AUTOMATED TOOL SELENIUM */

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.By;

public class Testing {

public static void main(String[] args) {
System.setProperty("webdriver.chrome.driver", "path of the exe file\\chromedriver.exe");
System.setProperty("webdriver.firefox.driver", "path of the exe file\\firefoxdriver.exe");

//initialization
   WebDriver drivers = new FirefoxDriver(), new ChromeDriver(), new InternetExplorerDriver() ;
   String Url = "Website\index.html";

// launch firefox and chrome and open up Website
   drivers.get(Url);

// Checking if the title is correct
   String expected = "Terms and Conditions Analyser"
   String actual = drivers.getTitle();

   if(expected.equals(actual)) {

     System.out.println("Displayed correct website title");

   } else {

     System.out.println("Displayed incorrect website title");
   }

// Checking buttons
   WebElement TopHeader = drivers.findElement(By.id("Top"));
   TopHeader.click();

   WebElement AboutHeader = drivers.findElement(By.id("About"));
   AboutHeader.click();

   WebElement TextAreaDirector = drivers.findElement(By.id("Analyse Ts and Cs"));
   TextAreaDirector.click();

// Text area for user to submit their contracts in
   WebElement TextArea = drivers.findElement(By.name("Terms and Conditions"));
   TextArea.sendKeys("We may disclose information where we are required to do so by law, for example, in response to a court order or a subpoena, or where we disclose information to data processors who act on our behalf (service providers or other group companies who provide support for the operations of our website and who do not use or disclose the information for any other purpose). To the extent permitted by applicable law");

// Find and check if Analyse submits text to the API to be analysed

   WebElement Analyse = drivers.findElement(By.id("Analyse"));
   Analyse.click();
   System.out.println("Your text was successfully analysed");

// Clear text area
   WebElement ClearText = drivers.findElement(By.id("ClearText"));
   if(ClearText.click()){
     TextArea.clear();
     System.out.println("You have successfully cleared text off the area");
   } else {
     System.out.println("You havent successfully cleared text off the area");
   }

// close browser and terminate java program

  drivers.close()
  System.out.println("Test completed");
  System.exit(0);
}


}
