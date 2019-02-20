# 3rd quiz of the course.

Well known breast cancer database, Wisconsin Breast Cancer Database, or WBC Database,
containing 10 attributes including a class label (benign and malignant) of 699 instances.

The attribute and domain information of WBC database is given below:

ID       Description                     Domain

-attr1   Clump Thickness                 1 - 10

-attr2   Uniformity of Cell Size         1 - 10

-attr3   Uniformity of Cell Shape        1 - 10

-attr4   Marginal Adhesion               1 - 10

-attr5   Single Epithelial Cell Size     1 - 10

-attr6   Bare Nuclei                     1 - 10

-attr7   Bland Chromatin                 1 - 10

-attr8   Normal Nucleoli                 1 - 10

-attr9   Mitoses                         1 - 10

Class                           benign & malignant


# Cleaning WBC Database
There  are  21  missing  attribute  values  (denoted  by  ‘?’)   in  modified  WBC
database.  In this phase program remove and replace them with the appropriate values.

# Retrieving knowledge from WBC dataset
This phase is constructed on a scenario where program take sample from an imaginary patient
that is necessary for the diagnosis of breast cancer. Instead of having exact values, program have only conditions containing
i)relational operators and
ii)numeric values to  calculate  the probability of him/her to show symptoms of breast cancer.

#       Operator        Description
1       <               less than
2       <=              less than or equal to
3       >               greater than
4       >=              greater than or equal to
5       !=              not equal to
6       =               equal to
7       ?               any value


Program run with command-line argument within the following formar:
        python 1.py <:11,!=:0,>=:1,>:5,?,?,<=:9,>:2,?
        
