#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Take the command line argument and read the text file 
void read_input(char *file_name, char protein[]){
    FILE *fptr;
    if ((fptr = fopen(file_name, "r")) == NULL){
        printf("There is no file named %s\n", file_name);
        exit(0);}
    fscanf(fptr, "%s", protein);
    if (strlen(protein) == 0){
        printf("File is empty!\n");
        exit(0);}
}

// Check the nucleotides and check they are wheter amino acid or not
char check_aminoacid(char codon[]){

    if (codon[2] != 'C' && codon[2] != 'U' && codon[2] != 'A' && codon[2] != 'G'){
        printf("It's not a known protein.\nIt is probably a new protein.\n");
        exit(0);}

    if (codon[0] == 'C'){
        if (codon[1] == 'U')
        {
            return 'L';
        }
        
        else if (codon[1] == 'C')
        {
            return 'P';
        }
        
        else if (codon[1] == 'G')
        {
            return 'R';
        }
        
        else if (codon[1] == 'A')
        {
            if ( codon[2] == 'U' || codon[2] == 'C')
            {
                return 'H';
            }
            else
            {
                return 'Q';
            }
        }
    }

    
    else if (codon[0] == 'A')
    {
        if (codon[1] == 'U')
        {
            if (codon[2] == 'G'){
                return 'M';
            }
            else{
                return 'I';
            }
        }
        
        else if (codon[1] == 'C')
        {
            return 'T';
        }
        
        else if (codon[1] == 'A')
        {
            if (codon[2] == 'U' || codon[2] == 'C'){
                return 'N';
            }
            else{
                return 'K';
            }
        }
        
        else if (codon[1] == 'G')
        {
            if ( codon[2] == 'U' || codon[2] == 'C'){
                return 'S';
            }
            else{
                return 'R';
            }
        }
    }

    else if (codon[0] == 'G')
    {
        if (codon[1] == 'U'){
            return 'V';
        }
        
        else if (codon[1] == 'C')
        {
            return 'A';
        }
        
        else if (codon[1] == 'G')
        {
            return 'G';
        }
        
        else if (codon[1] == 'A')
        {
            if (codon[2] == 'U' || codon[2] == 'C'){
                return 'D';
            }
            else{
                return 'E';
            }
        }
    }
    
    else if (codon[0] == 'U')
    {
        if (codon[1] == 'U'){
            if ( codon[2] == 'U' || codon[2] == 'C'){
                return 'F';
            }
            else{
                return 'L';
            }
        }
        
        else if (codon[1] == 'C')
        {
            return 'S';
        }
        
        else if (codon[1] == 'A' && (codon[2] == 'U' || codon[2] == 'C'))
        {
            return 'Y';
        }
        
        else if (codon[1] == 'G')
        {
            if (codon[2] == 'U' || codon[2] == 'C'){
                return 'C';
            }
            else if (codon[2] == 'G')
            {
                return 'W';
            }
        }
    }
    printf("It's not a known protein.\nIt is probably a new protein.\n");
    exit(0);
}

// Check the start and stop codons
int check_start_stop(char protein[]){
    char start_codon[4] = {protein[0],protein[1],protein[2]};
    char stop_codon[4] = {protein[27],protein[28],protein[29]};
    if (strcmp(start_codon,"AUG") != 0){
        return 'i';}
    else if (((strcmp(stop_codon,"UAA") == 0) || (strcmp(stop_codon,"UAG") == 0) || (strcmp(stop_codon,"UGA") == 0)) == 0){
        return 'f';}
    else{return 1;}
}

// Check is the given protein match with known proteins
char check_protein(char shortened_protein[]){
    char myProtA[10] = "MVAEGTKRI";
    char myProtB[10] = "MGEAVRKTI";
    char myProtC[10] = "MFSYCLPQR";
    char myProtD[10] = "MFLVPTYDH";
    char myProtE[10] = "MFSYCLPKR";

    if (strcmp(shortened_protein, myProtA) == 0){
        return 'A';
    }
    
    else if (strcmp(shortened_protein, myProtB) == 0)
    {
        return 'B';
    }
    else if (strcmp(shortened_protein, myProtC) == 0)
    {
        return 'C';
    }
    else if (strcmp(shortened_protein, myProtD) == 0)
    {
        return 'D';
    }
    else if (strcmp(shortened_protein, myProtE) == 0)
    {
        return 'E';
    }
    return 'X';

}

// Print the proteins as the given format
void print_protein(char *protein){
    for (int i = 0; i <= strlen(protein)-1; i++){
        printf("%c", protein[i]);
        if (i == strlen(protein)-1){
            printf("\n");
            break;}
        printf("-");
    }
}

// Main function executes the other functions with arguments that they need
int main(int argc, char *argv[])
{
    char protein[31];
    if (argc != 1){
        read_input(argv[1], protein);
    }
    else{
        printf("Enter the input file!\n");
        exit(0);}
    
    char result = check_start_stop(protein);
    if ( result == 'i' ){
        printf("No start with AUG it is not a protein\n");
        exit(0);
    }
    else if ( result == 'f'){
        printf("It's not a protein! No Stop code\n");
        exit(0);
    }
    
    int j = 0;
    char shortened_protein[10];
    for(int i = 0; i < (strlen(protein))-3;){
        char codon[4] = {protein[i],protein[i+1],protein[i+2]};
        char aminoacid = check_aminoacid(codon);
        shortened_protein[j] = aminoacid;
        i += 3;
        j++;
    }
    
    char protein_name = check_protein(shortened_protein);
    if (protein_name == 'X'){
        printf("It is not a known protein.\n\nIt is probably a new protein.\n");
        exit(0);
    }
    printf("MyProtein%c idedtified in sequence.\n\nThe amino acids of MyProtein%c: ", protein_name, protein_name);
    print_protein(shortened_protein);
    printf("protein%c: ", protein_name);
    print_protein(shortened_protein);

    return 0;
}

