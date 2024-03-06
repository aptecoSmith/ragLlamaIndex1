# Introduction

### What is an audience?

An audience refers to a specific group of individuals or companies. These individuals share common characteristics, interests, or behaviours, that make them relevant and receptive to marketing efforts. Orbit allows you to better understand your audience and target them for marketing campaigns or messages.

An audience can be defined and segmented based on various characteristics.


Orbit provides a very flexible and powerful way of defining your audience, allowing you to combine these factors in many ways. 

To create an Audience, first navigate to the Audiences area by clicking on the word 'Audiences' on the Global Header.
Here you will see a list of all existing audiences.
There are options to search and filter these audiences, or, if you want to create a new Audience, click on the blue '+ New Audience' button.

**Note** There is also a tile on the Home screen marked 'Create Audience' that will ask you to input your new Audience's name, then immediately take you to the Audience ready for editing.

Once you have clicked on the '+ New Audience' button, you will be prompted to name your new Audience.  Once you have done so, click the blue Create button. 

Once this is done, you will be taken to what we refer to as a 'Workbook'.  You may see this sometimes called an 'Audience Workbook'.

The first tab of a workbook is always an 'audience tab' and this is where you will land.  This is where you will define what selection of criteria you want.

On screen, the UI is broken down into a number of areas.
At the top you can see the name of your audience that you supplied earlier.
Underneath is a row of information, starting with a grey badge which at this point will say 'Unsaved'.
Next to that is the Total Audience Count label, which stands out in blue.
The count is very important as it signifies how many records in your database meet the criteria that you have selected.
At this point, you have not selected any criteria, so the count says 0.
Next to that should be a dropdown that is currently set to your default Table.
The tables structure for your system will hopefully already be known to you.   Whichever Table you select here is what you are ultimately counting.
For example if you have a table of Customers, one of Products, and one of Purchases, then you would see these three options available.
It is important to note that you must set the Table before you add selection criteria.
Next to that is a percentage indicator.
Next to that is a bar chart representation of the percentage.
And finally there is a button to Apply Limits to your selection.
All these elements sit under the audience name textbox.
On the right of the screen should be a blue Save button that is currently disabled, and an ellipsis button that shows some audience options.
These options are: Rename, Show Brief, Duplicate, Close and Delete.

Underneath the Count row, is the Tabs interface.  Currently you will see the Audience tab is the only tab.  Next to it, is a disabled 'Add New' button.
This is to add a new tab.  It is currently disabled, because you must have some records counted to enable it.

On the Audience tab, there are two subsections, Excludes and Includes.  You will see that Excludes is folded away but Includes is expanded.
Next to the titles of each section there is a zero, indicating no records are currently included in either section.
In the expanded Includes section, you will see a bar we call an Audience Node.
Each node defines one particular criteria, and Nodes can be AND or OR linked logically, as well as dragged to change the order of application.
This first Node has a special tickbox option of Include All.  Ticking it will select all the records on this Table.  
The count will update both on the Total Audience count, and the Includes Section Count.

Next to the tickbox label is a button marked 'Add Filter' which will open the System Search dialog.
This dialog is where you can select the variables on the different tables, and this is setup as a tree.
For example if you have a Customers table, then there will be a tree node within the dialog for Customers.
Expanding it will show the variables available.  Typically these variables correspond to information known about your customers.
Examples include a unique reference number or URN, Forename, Surname, Title, Gender etc.
Similarly we might know things like their age, their occupation, where they live, what car they drive or their yearly income.
If these Customers have shopped with us then those transactions may be recorded on a Transactions Table.
The categories available on such a table would include a unique reference number or URN, the date of the transaction, the value of the purchases and what products were purchased.
Finally we might have a Product table, which includes, as well as a URN, a Description, a category, a weight, price, manufacturing origin, colour, style etc.

If for our marketing purposes we wanted to identify customers in our database who in the last year had purchased umbrellas,
we would ensure the Audience was set to the Customers table.
Add a filter of Purchase date from the Transactions table, and fill out the Date Picker UI to ensure it returned Transactions from the last Year.
THere should be more information available for the Date Variable Interface which was recently improved to make defining exactly the date period you want easier.
Once you have defined your date period and you will see the Node has updated.
It no longer offers the option to select All Records.
The variable 'Transaction Date' will be shown along with a calendar icon to denote it is a Date variable.
The text 'is any of' denotes your choice in the Date Picker UI to include records in this date range.
You should then see a white chip with a shorthand description of the date range picked, for example:
Every 1 day(s) backwards by one year
There is then an 'Add Values' button in case you want to reopen the DatePicker UI, and finally a red bin icon, where you can delete the node altogether.
You should see the Count update accordingly.
Well done!  You have just created your first Audience!  You will notice that now the audiences is valid the Save button has become enabled.
Click Save, and the button will disable again until you make some changes.

If you hover over the audience node you will notice two blue buttons appear underneath the variable name.
These are the node addition buttons And and OR.
We have narrowed our Customer selection down to the time period we were interested in, but now we need to narrow down the product purchased.
Click the small blue 'And' button to add another Audience node underneath the first.
You will see this new node does not have an option to select all People, but it does have an 'Add Filter' button.
Click on 'Add Filter' to open the System Search dialog.
You could navigate through the tree to find the product category, or you could type into the search box 'Umbrella'.
By default the system search returns variables, but you will see there is a tick box marked 'Include codes in search'.
If you tick this the results will now show matching categories within variables.
As such, you should see an option something like Product Category - Umbrella.
Clicking this will update the System Search UI as if you had clicked through the tree to select the Product Category Variable,
and it now selects umbrella.  Click Apply to Apply this choice to your audience.

You should notice the count has reduced.  This audience now defines Customers in your database who purchased an umbrella in the last year.

You may wish to limit your audience to a certain number of records.  This can be done after your nodes have been created, by clicking the Apply Limits button.












You can define your audience via the **Audience** tab.



