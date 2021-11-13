# Project Requirements Feedback

## Requirements Specification
 - Stakeholders not identified.

## Use cases
### Alternative paths
Alternative paths should outline what can cause the alternative path and what actions will be taken by the software if they result.

### Overspecification
Your use cases and requirements should avoid specifying a design. You expllicitly state as a use case (create application frameowrk code) that Flask must be used. Overall, that is not a use case, but more appropriately would be a development task. Remember that use-cases are the interaction case that a user would have with your software.

### Actions
Actions are the explanation of the transactional interaction between a user and the software. In many cases throughout your use cases, that isn't very reflected well. Am example of what this means is that say a user wants to log in. The actions would look something like
 - The user indicates to the software they wish to log in
 - The software prompts the user to input their login information
 - The user provides their log in information
 - The software validates the user with the provided information and redirects to the landing page.
 You have an example of doing this well in "Create Account", but other use cases get a bit less descriptive and don't have that same structure.