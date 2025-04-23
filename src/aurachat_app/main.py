from view_controllers.main_viewcontroller import MainViewController

def main():
    controller = MainViewController()
    
    # Example of updating the UI
    controller.update_status("Lets gooo!")
    controller.update_title("AuraChat Bot - Active")
    
    controller.run()
    

if __name__ == "__main__":
    main()
