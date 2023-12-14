#include<bits/stdc++.h>
using namespace std;

#include "lcgrand.h"

#define BUSY 1
#define IDLE 0

ofstream event_orders("event_orders.txt");
ofstream result("results.txt");
double event_time_min; 

double next(double mean) 
{
    return -mean * log(lcgrand(4));
}

//initialization variables
double simulation_time,total_delays, area_num_people_in_queue, area_server_utilization;
int server_state, num_customer_in_queue, num_customer_delayed;
double next_arrival_time, next_departure_time;
double mean_interarrival_time, mean_service_time, total_delays_required;
int total_event;
//arrival variables
queue<double> arrival;
int next_event_type; // 1 for arrival, 2 for departure
//timing variables
int arriver_customer, depart_customer;
double last_event_time;
//calculation variables
double time_passed;

double simulation_time_given;
int q_limit_given;
int bulked_customer = 0;

void start()
{
    simulation_time = 0.0;
    server_state = IDLE;
    num_customer_in_queue = 0;
    num_customer_delayed = 0;
    total_delays = 0.0;
    area_num_people_in_queue = 0.0;
    area_server_utilization = 0.0;
    next_arrival_time = simulation_time + next(mean_interarrival_time);
    next_departure_time = 1.0e+30; // to avoid infinite loop
    total_event = 0;
    arriver_customer = 0;
    depart_customer = 0;
    last_event_time = 0.0;
}
void results_file()
{
    //set precision
    result<<fixed<<setprecision(6);
    result<<"----Single-Server Queueing System----\n"<<endl;
    result<<"Mean inter-arrival time: "<<mean_interarrival_time<<" minutes" <<endl;
    result<<"Mean service time: "<<mean_service_time<<" minutes" <<endl;
    result << "Maximum Queue Length: " << q_limit_given << endl;

    result<<"\nAvg delay in queue: "<<total_delays/num_customer_delayed<<" minutes" <<endl; 
    result<<"Avg number in queue: "<<area_num_people_in_queue/ceil(simulation_time)<<endl; 
    result<<"Server utilization: "<<area_server_utilization/(simulation_time) <<endl; 
    result<<"Time simulation ended: "<<ceil(simulation_time)<<" minutes" <<endl; 

    result << "\nTotal number of Balking customers: " << bulked_customer << endl;
    result << "Total number of customers delayed: " << num_customer_delayed << endl;
    result << "Percentage of Balking customers: " << (double)bulked_customer / (double)(num_customer_delayed+bulked_customer) * 100 << " %" << endl;
}


void find_next_event()
{
    total_event++;

    if (next_arrival_time <= next_departure_time)
    {
        event_time_min = next_arrival_time;
        next_event_type = 1; 
        arriver_customer++;
        event_orders<< total_event << ". Next event: Customer " << arriver_customer << " Arrival" << endl;
    }

    else
    {
        event_time_min = next_departure_time;
        next_event_type = 2; 
        depart_customer++;
        event_orders<< total_event << ". Next event: Customer " << depart_customer << " Departure" << endl;
    }

    if(event_time_min > simulation_time_given)
    {
        results_file();
        exit(0);
    }


    simulation_time = event_time_min; // advance the clock
}



void customer_arrival()
{
    next_arrival_time = simulation_time + next(mean_interarrival_time); 

    if(server_state == BUSY)
    {
        if(num_customer_in_queue < q_limit_given)
        {
            num_customer_in_queue++;
            arrival.push(simulation_time);
        }
        else
        {
            bulked_customer++;
            event_time_min = next_departure_time;

            //event_orders<< "Customer " << bulked_customer << " is bulked" << endl;
        }
    }

    else
    {
        server_state = BUSY;
        num_customer_delayed++;
        event_orders << "\n---------No. of customers delayed: "<< num_customer_delayed << "--------\n" <<endl;
        next_departure_time = simulation_time + next(mean_service_time);
    }
}


void customer_departure()
{
    double delay;
    if(num_customer_in_queue == 0)
    {
        server_state = IDLE;
        next_departure_time = 1.0e+30; 
    }

    else
    {
        num_customer_in_queue--; 
        delay = simulation_time - arrival.front();
        arrival.pop();
        total_delays += delay ; 
        num_customer_delayed++; 
        event_orders << "\n---------No. of customers delayed: "<< num_customer_delayed << "--------\n" <<endl;
        next_departure_time = simulation_time + next(mean_service_time); 
    }

}



void calculation_metrics()
{
    time_passed = simulation_time - last_event_time; // find the time consumed since last event
    last_event_time = simulation_time;

    area_num_people_in_queue = area_num_people_in_queue + num_customer_in_queue * time_passed; 
    area_server_utilization = area_server_utilization + server_state * time_passed; 
}


int main()
{
    ifstream fin("in.txt");
    fin>>mean_interarrival_time>>mean_service_time>>simulation_time_given>>q_limit_given;
    fin.close();

    start();

    while (simulation_time <= simulation_time_given)
    {
        find_next_event();
        calculation_metrics();
        if(next_event_type == 1)
            customer_arrival();
        else if(next_event_type == 2)
            customer_departure();
    }

    results_file();


}