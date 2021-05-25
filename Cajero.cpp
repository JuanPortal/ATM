#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <cstdlib>
#include <conio.h>
#include <string>
#define pass "1201"
using namespace std;
float deposito(float *p);
float retiro(float *p);
float dep,ret,recibo,trans;
struct Usuarios
{
	char Usuario[5];
	float Saldo;
};
float deposito(float *p)
{
	*p=*p+dep;
}
float retiro(float *p)
{
	*p=*p-ret;
}
float pagotarjeta(float *p)
{
	*p=*p-49.9;
}
float servicios(float *p)
{
	*p=*p-29.9;
}
float transferencia(float *a,float *b)
{
	*a=*a-trans;
	
	*b=*b+trans;
}
int buscarPorNombre(char *nombre, Usuarios *Usuario)
{
	for (int i=0;i<5;i++)
	{
		if ( strcmp(Usuario[i].Usuario,nombre)==0 ) 
		{
			return i;
		}
	}
	return -1;
} 
int main() 
{
	string password;
	int contador=0;
	bool ingreso=false;
	struct Usuarios usu,Usuario[5];
	int i,opcion=1,option=1;
	float Saldo;
	for (int i=0;i<5;i++)
	{   
		printf("Introduzca el nombre del Cliente: ");
		scanf("%s", Usuario[i].Usuario);
		fflush(stdin);
		printf("Introduzca el saldo: ");	
		scanf("%f",&Usuario[i].Saldo);
		printf("\n");
	}	
	cout<<"================================"<<endl;
    do
    {
    	system("cls");
		printf("INGRESE USUARIO : ");  
		scanf("%s", usu.Usuario);
		cout<<"INGRESE CONTRASE"<<char(165)<<"A : ";
		char asterisco;
		asterisco=getch();
		password=="";
		while (asterisco!=13) //Mientras asterisco sea diferente de la tecla Enter
		{
			if (asterisco== 8)
			{
        		if (password.length() > 0)
				{
					password = password.substr(0, password.length() - 1);
	            	cout << "\b \b"; 
				}
 			}
			else
			{
	    		password.push_back(asterisco);
	    		cout << "*";
    		}   
        	asterisco = getch();
		}
		if (password==pass)
		{
			ingreso=true;
		}
		else
		{
			cout<<"\nContrase"<<char(164)<<"a incorrecta"<<"\n"<<endl;
			contador++;
		}
	}
	while (ingreso==false && contador<3);
	if (ingreso==false)
	{
		cout<<"\nNo se puedo ingresar al sistema"<<"\n"<<endl;
	}
	else
	{
		for( int i=0;i<5;i++)
		{
			if ( strcmp(Usuario[i].Usuario,usu.Usuario)==0 )
			{					
			    cout<<"\n"<<endl;
				cout<<"   __________________________________________________________________"<<endl;
			    cout<<"   |                                                                |"<<endl;
				cout<<"   |                BIENVENIDO AL CAJERO AUTOM"<<char(181)<<"TICO                 | "<<endl;
			    cout<<"   |________________________________________________________________|"<<endl;
				while ( (opcion==1 || opcion==2 || opcion==3 || opcion==4 || opcion==5) && (opcion!=6))
				{
					cout<<"                                   "<<endl;	
					cout<<".......SELECCIONE UNA OPCI"<<char(224)<<"N....... "<<endl;
				    cout<<"                                   "<<endl;	
					printf("\n(1) Consultar Saldo\n");
					cout<<"(2) Hacer un dep"<<char(162)<<"sito\n";
					printf("(3) Hacer un retiro\n");
					printf("(4) Hacer un pago de servicios\n");
					printf("(5) Hacer una transferencia\n");
					printf("(6) Salir\n");
					cout<<"\nIntroduzca una opci"<<char(162)<<"n: ";
					scanf("%d",&opcion);
					cout<<"\n";
					if (opcion==1)
					{
						printf("\nCliente: %s\n",Usuario[i].Usuario);
						printf("\nSaldo: %f\n",Usuario[i].Saldo);
						cout<<endl;  	
					}
					else if(opcion==2)
					{
						cout<<"\nIngrese la cantidad a depositar: ";
						cin>>dep;
						deposito(&Usuario[i].Saldo);
						cout<<"\nEL dep"<<char(162)<<"sito se realiz"<<char(162)<<" exitosamente"<<endl;
						cout<<"\nEl nuevo saldo es: "<<Usuario[i].Saldo<<endl;
					}
					else if(opcion==3)
					{
						cout<<"\nIngrese la cantidad a retirar: ";
						cin>>ret;
						if (Usuario[i].Saldo>=ret)
						{
						   	retiro(&Usuario[i].Saldo);
							cout<<"\nEL retiro se realiz"<<char(162)<<" exitosamente"<<endl;
							cout<<"\nEl nuevo saldo es: "<<Usuario[i].Saldo<<"\n"<<endl;
						}
						else
						{
						   	cout<<"\nNo cuenta con saldo suficiente para realizar esta operaci"<<char(162)<<"n"<<endl;
						}
					}
					else if(opcion==4)
					{
						while ( (option==1 || option==2 || option==3) && (option!=4))
						{
							printf("1. Pagar tarjeta.\n");
							printf("2. Pagar recibo de agua.\n");
							printf("3. Pagar recibo de luz.\n");
							printf("4. Retroceder\n");
							cout<<"\nIntroduzca una opci"<<char(162)<<"n: ";
							scanf("%d",&option);
							if(option==1)
							{
								cout<<"\nEl monto del mes es 49.9 nuevos soles"<<endl;
							 	if (Usuario[i].Saldo>=49.9)
								{
									pagotarjeta(&Usuario[i].Saldo);
									cout<<"\nEl nuevo saldo es: "<<Usuario[i].Saldo<<"\n"<<endl;
								}
								else
								{
									cout<<"\nNo cuenta con saldo suficiente para realizar esta operaci"<<char(162)<<"n"<<"\n"<<endl;
								}						
							}
							else if (option==2 || option==3)
							{
								cout<<"\nEl monto del mes es 29.9"<<endl;
								if ( strcmp(Usuario[i].Usuario,usu.Usuario)==0 )
								{
									if (Usuario[i].Saldo>=29.9)
									{
										servicios(&Usuario[i].Saldo);
										cout<<"\nEl nuevo saldo es: "<<Usuario[i].Saldo<<"\n"<<endl;
									}
									else
									{
										cout<<"\nNo cuenta con saldo suficiente para realizar esta operaci"<<char(162)<<"n"<<"\n"<<endl;
									}
								}
							}
							else
							{
								int main;
							}
						}
					}
					else if(opcion==5)
					{
						int idxUsuarioDeposito = buscarPorNombre(usu.Usuario, Usuario);
						printf("Transferir a: ");
						scanf("%s", usu.Usuario);
			            int idxUsuarioTransferir = buscarPorNombre(usu.Usuario, Usuario);
						cout<<"\nLa cantidad de: ";
						cin>>trans;
						if (trans<=Usuario[i].Saldo)
						{
							transferencia(&Usuario[idxUsuarioDeposito].Saldo, &Usuario[idxUsuarioTransferir].Saldo);
							cout<<"\nTransferencia exitosa"<<endl;
							cout<<"\nEl nuevo saldo es: "<<Usuario[idxUsuarioDeposito].Saldo<<"\n"<<endl;
						}
						else
						{
							cout<<"\nNo cuenta con saldo suficiente para realizar esta operaci"<<char(162)<<"n"<<"\n"<<endl;
						}
						printf("\n\n\n");
					}
					else
					{
						cout<<"\nGracias por su visita"<<endl;
					}	
				}
			}
			else
			{
				cout<<" "<<endl;	
			}
		}
	}
system("pause");	
}
