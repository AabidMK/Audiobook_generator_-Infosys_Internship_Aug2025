# Extracted Text + OCR

 
 
 
 
DEPARTMENT  OF COMPUTER  SCIENCE  AND  ENGINEERING  
 
 
 
 
NOTES  
 
 
CLOUD  COMPTING  
SUBJECT  CODE:  22SCF71/2 2SCS71/2 2SAL71  
 
 
 
 
 
 
 
 
COMPILED  BY 
 
K Madhusudha  
 
2025-26 
 
 
CC (22SCF/SCS/SAL71 ) Page  1 
 
SRINIVAS  UNIVERSITY  
INSTITUTE  OF ENGINEERING  AND  TECHNOLOGY  
MUKKA,  MANGALURU   
 
 
 
Syllabus:                MODULE  I 
Introduction  to Cloud  Computing  
Introduction,  Cloud  Computing  at a Glance,  The Vision  of Cloud  Computing,  Defining  a Cloud,  A Closer 
Look, Cloud Computing Reference Model, Characteristics and Benefits, Challenges Ahead, Historical 
Developments, Distributed Systems, Virtualization, Web 2.0, Service -Oriented Computing, Utility - 
Oriented  Computing,  Building  Cloud  Computing  Environments,  Application  Development,  Infrastructure 
and System Development, Computing Platforms and Technologies, Amazon Web Services (AWS), 
Google App Engine, Microsoft Azure, Hadoop, Force.com and Salesforce.com, Manjra soft Aneka 
Virtualization, Introduction, Characteristics of Virtualized, Environments Taxonomy of Virtualization 
Techniques,  Execution  Virtualization,  Other  Types  of Virtualization,  Virtualization  and Cloud  Computing, 
Pros and Cons of Virtualization, Technology Examples Xen: Para virtualization, VMware: Full 
Virtualization, Microsoft Hyper -V. 1.1 Introduction  
Computing is being transformed into a model consisting of services that are commoditized and delivered 
in a manner  similar  to utilities  such as water,  electricity,  gas, and telephony.  In such a  model,  users access 
services based on their requirements, regardless of where the services are hosted. Cloud computing is the 
most recent emerging paradigm promising to turn the vision of “computing utilities” into a reality.  
Cloud computing is a technological advancement it is based on the concept of dynamic provisioning , 
which  is applied  not only to  services  but also to compute  capability,  storage,  networking, and  information 
technology (IT) infrastructure in general. Resources are made available through the Internet and offered 
on a pay-per-use basis from cloud  computing vendors.  
1.2 Cloud  computing  at a glance  
In 1969,  Leonard  Kleinrock,  one of the chief  scientists  of the original  Advanced  Research  Projects  Agency 
Network (ARPANET), which seeded the Internet, said:  
As of now,  computer  networks  are still in their  infancy,  but as they grow  up and become  sophisticated,  we 
will probably  see the spread  of ‘computer  utilities’  which,  like present  electric  and telephone  utilities,  will 
service individual homes and offices across the  country.  
Cloud  computing  allows  renting  infrastructure,  runtime  environments,  and services  on a pay- per-use basis. 
End users leveraging cloud computing services can access their documents and data anytime, anywhere, 
and from any device connected to the Internet. One of the most diffuse views of cloud computing can be 
summarized as follows:  
I don’t  care where  my servers  are, who manages  them,  where  my documents  are stored,  orwhere 
my applications  are hosted.  I just want  them  always  available  and access  them  from  any device  connected 
through Internet. And I am willing to pay for this service for as a long as I needit.  
Web 2.0 technologies  play a central  role in making  cloud  computing  an attractive  opportunity  forbuilding 
computing systems. Service orientation allows cloud computing to deliver its capabilities with familiar 
abstractions, while virtualization confers on cloud computing thenecessary degree of customization, 
control, and flexibility for building production and enterprise systems.  
1.3 The vision of  cloud  computing  
Cloud computing allows anyone with a credit card to provision virtual hardware, runtime environments, 
and services. These are used for as long as needed, with no up -front commitments required. The entire 
stack of a computing system is transformed into a collection of utilities, which can be provisioned and 
composed together to deploy systems in hours rather  than days and with virtually  no maintenance costs.   
Figure  1.1 Cloud  computing vision  
 
Previously,  the lack of effective  standardization  efforts  made  it difficult  to move  hosted  services from  one 
vendor to another. The long -term vision of cloud computing is that IT services are traded as  utilities  in 
an open market, without technological and legal barriers. In this cloud marketplace, cloud service 
providers  and consumers, trading  cloud  services  as utilities,  play a central  role. Many  of the technological 
elements  contributing  to this vision  already  exist.  The capability  for Web - based  access  to documents  and 
their processing using sophisticated applications is one of the appealing factors for end users. Vision of 
cloud  computing  is that in the near future  it will be possible  to find the solution  that matches  the customer 
needs by simply entering our request in a global digital market that trades cloud computing services.  
1.4 Defining  a cloud  
The Internet plays a fundamentalrole in cloud computing, since it represents either the medium or the 
platform through which many cloud computing services are delivered  and made accessible. This aspect  
is also reflectedin the definition given by Armbrust:  
Cloud  computing  refers  to both the applications  delivered  as services  over the Internet  and the hardware 
and system software in the datacenters that provide those services.  
This definition describes cloud computing as a phenomenon touching on the entire stack: from the 
underlying hardware to the high -level software services and applications. It introduces the concept of 
everything as a service , mostly referred as XaaS , where the different components of a system —IT 
infrastructure,  development  platforms,  databases,  and so on—can be delivered,  measured,  and 
consequently priced as a service. The approach fostered by cloud computing is global. This notion of 
multiple parties using a shared cloud computing environment is highlighted in a definition proposed by 
the U.S. National Institute of Standards and Technology (NIST):  
Cloud computing is a model for enabling ubiquitous, convenient, on -demand network accessto a 
shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and 
services) that can be rapidly provisioned and released with minimal management effort or service 
provider interaction.  
According to Reese, we can define three criteria to discriminate whether a service is deliveredin the cloud 
computing style:  
The service is accessible via a Web browser (nonproprietary) or a Webservices application 
programming interface (API).  
Zero  capital  expenditure  is necessary  to get started. 
You pay only for what you use as you use it.  
The utility -oriented  nature  of cloud  computing  is clearly  expressed  by Buyya:  
A cloud is a type of parallel and distributed system consisting of a collection of interconnected and 
virtualized  computers  that are dynamically  provisioned  and presented  as one or more  unified  computing 
resources based on service -level agreements established through negotiation between the service 
provider and consumers . 
1.5 A closer look  
Cloud computing is helping enterprises, governments, public and private institutions, and research 
organizations shape more effective and demand -driven computing systems. Practical examples of such 
systems exist across all market segments:  
Large enterprises can offload some of their activities to cloud -based systems. Recently, the New York 
Times has converted its digital library of past editions into a Web -friendly format. This required a 
considerable  amount  of computing  power  for a short  period  of time.  By renting  Amazon  EC2 and S3 Cloud 
resources, the Times performed this task in 36 hours and relinquished these resources, with no additional 
costs.  
Small enterprises and start -ups can afford to translate their ideas into business results more quickly, 
without excessive up -front costs . Animoto is a company that createsvideos out of images, music, and 
video fragments submitted by users. The process involves a considerable amount of storage and backend 
processing  required  for producingthe  video,  which is  finally  made  available  to the user.  Animoto  does not 
own a single server and bases its computing infrastructure entirely on Amazon Web Services.  
System  developers  can concentrate  on the business  logic  rather  than  dealing  with the complexity  of infrastructure  management  and scalability . Little  Fluffy  Toys is  a company in London that has developed 
a widget  providing  users  with information  about nearby  bicycle  rental  services.  The company  has managed  to back 
the widget’s computing needs on Google AppEngine and be on the market in only one week.  
End users can have their documents accessible from everywhere and any device. AppleiCloud is a 
service that allows users to have their documents stored in the Cloud and access them from any device 
users connect to it.  
Cloud  computing  does not only contribute  with the opportunity  of easily  accessing  IT services  ondemand, 
it also introduces a new way of thinking about IT services and resources: as utilities. The three major 
models for deploying and accessing cloud computing environments are public clouds, private/enterprise 
clouds, and hybrid clouds.  
Public clouds are the most common deployment models in which necessary IT infrastructure (e.g., 
virtualized datacenters) is established by a third -party service provider that makes itavailable to any 
consumer on a subscription basis. Such clouds are appealing to users because they allow users to quickly 
leverage compute, storage, and application services. In this environment, users’ data and applications are 
deployed on cloud datacenters on the vendor’s premises.  
Large  organizations  that own massive  computing  infrastructures  can still benefit  from  cloud  computing  by 
replicating  the cloud  IT service  delivery  model  in-house.  This idea has given  birth  to the concept  of private 
clouds  as opposed  to public  clouds.  In 2010,  for example,  the U.S. federal  government,  one of the world’s 
largest consumers of IT spending started a cloud computing initiative aimed at providing government 
agencies  with a more  efficient  use of their computing  facilities.  The use of cloud -based  in-house  solutions 
is also driven by the need to keepconfidential information within an organization’s premises. Institutions 
such as governments andbanks that have high security, privacy, and regulatory concerns prefer to build 
and use their own private or enterprise clouds.  
Whenever private cloud resources are unable to meet users’ quality -of-service requirements, hybrid 
computing systems, partially composed of public cloud resources and privately owned infra - structures, 
are created to serve the organization’s needs. These are often referred as hybrid clouds , which are 
becoming a common way for many stakeholders to start exploring the possibilities offered by cloud 
computing.  
 
1.6 The Cloud  Computing  Reference  Model  
A fundamental characteristic of cloud computing is the capability to deliver, on demand, a variety of IT 
services that are quite diverse from each other. This variety creates different perceptions of what cloud 
computing is among users. Despite this lack of uniformity, it is possible to classify cloud computing 
services offerings into three major categories: Infrastructure -as-a-Service (IaaS) , 
Platform -as-a-Service  (PaaS) , and Software -as-a-Service  (SaaS) . 
These  categories  are related  to each  other  as described  in Figure  1.5 
 
Figure  1.2: Cloud  Computing  Reference  Model  
The model organizes the wide range of cloud computing services into a layered view that walks the 
computing stack from bottom to top.  
At the base of the stack, Infrastructure -as-a-Service solutions deliver infrastructure on demand in the 
form of virtual hardware , storage , and networking . Virtual hardware is utilized to provide compute on 
demand in the form of virtual machine instances. These are created at users’ request on the provider’s 
infrastructure,  and users  are given  tools  and interfaces  to configure  the softwarestack  installed  in the virtual 
machine. The pricing model is usually defined in terms of dollars perhour. Virtual storage is delivered in 
the form of raw disk space or object store. Virtual networking identifies the collection of services that 
manage  the networking among  virtual  instances  and their connectivity  to the Internet  or private  networks. 
Platform -as-a-Service solutions are the next step in the stack. They deliver scalable and elastic runtime 
environments on demand and host the execution of applications. These services are backed by a core 
middleware platform that is responsible for creating the abstract environment where applications are 
deployed  and executed. It  is the responsibility  of the service  provider  to provide  scalability  and to manage 
fault tolerance, while users are requested to focus on the logic of the application developed by leveraging 
the provider’s APIs and libraries. Thisapproach increases the level of abstraction at which cloud 
computing is leveraged but also constrains the user in a more controlled environment.  
At the top of the stack, Software -as-a-Service solutions provide applications and services on demand. 
Most of the common functionalities of desktop applications —such as office automation, document 
management, photo editing, and customer relationship management(CRM) software —are replicated on 
the provider’s  infrastructure  and made  more  scalable and accessible through a  browser  on demand. These  applications are shared across multiple users whose interaction is isolated  from the other users. The SaaS 
layer  is also the area of social  networking Websites, which leverage cloud -based infrastructures to sustain 
the load generatedby their popularity.  
Each layer provides a different service to users. IaaS solutions are sought by users who want to leverage 
cloud computing from building dynamically scalable computing systems requiring a specific software 
stack. IaaS services are therefore used to develop scalable Websites  or for back - ground processing.  
PaaS solutions provide scalable programming platforms for developing applications and are more 
appropriate when new systems have to be developed.  
SaaS  solutions  target  mostly  end users  who want  to benefit  from  the elastic scalability  of the cloud  without 
doing any software development, installation, configuration, and maintenance.  
1.7 Characteristics  and benefits  
Cloud computing has some interesting characteristics that bring benefits to both cloud service 
consumers (CSCs) and cloud service providers (CSPs). These characteristics are:  
• No up-front  commitments  
• On-demand  access  
• Nice  pricing  
• Simplified  application  acceleration  and scalability  
• Efficient  resource  allocation  
• Energy  efficiency  
• Seamless  creation  and use of third -party  services  
 
1.8 Challenges  ahead  
Challenges’  concerning  the dynamic  provisioning  of cloud  computing  services  and resources  
arises.  For example,  in the infrastructure -as-a-Service  domain,  how many  resources  need  to be provisioned, 
and for how long should  they be used,  in order  to maximize  the benefit?  Technical  challenges  also arise  for 
cloud  service  providers  for the management  of large  computing  infrastructures  and the use of virtualization 
technologies on top of them.  
Security in terms of confidentiality, secrecy, and protection of data in a cloud environment is another 
important challenge. Organizations do not own the infrastructure they use to process data and store 
information. This condition poses challenges for confidential data, which organizationscannot afford to 
reveal.  
Legal  issues may  also arise.  These  are specifically tied  to the ubiquitous  nature  of cloud computing, which 
spreads  computing  infrastructure  across  diverse  geographical  locations.  Different  legislation  about  privacy 
in different  countries  may potentially  create  disputes  as to the rights  that third  parties  (including  government 
agencies) have to your data.  1.9 Historical  Developments  
 
The idea of renting  computing  services by  leveraging  large  distributed  computing  facilities has  been  around  for long 
time.  It dates  back  to the days of the mainframes  in the early  1950s.  From  there  on, technology  has evolved  and been 
refined. This process has created a series of favorable conditions for the realization of cloud computing.  
The distributed computing technologies that have influenced cloud computing. In tracking the historical 
evolution,  we briefly  review  five core technologies that  played  an important role  in the realization of  cloud 
computing. These technologies are distributed systems, virtualization, Web 2.0, service orientation, and 
utility computing.  
1.9.1 Distributed Systems: Clouds are essentially large distributed computing facilities that make 
available  their services  to third  parties  on demand.  As a reference, we  consider  the characterization  of a 
distributed system proposed by Tanenbaum et al. [1]:  
A distributed  system  is a collection  of independent  computers  that appears  to its users  as a singlecoherent 
system.  
Three major milestones have led to cloud computing: mainframe computing, cluster computing, and grid 
computing.  
1.9.2 Mainframes. These were the first examples of large computational facilities leveraging multiple 
processing units. Mainframes were powerful, highly reliable computers specialized for large data 
movement and massive input/output (I/O) operations. They were mostly used by large organizations for 
bulk data processing tasks such as online transactions, enterprise resource planning, and other operations 
involving the processing of significant amounts of data. One ofthe most attractive features of mainframes 
was the ability to be highly reliable computers that were “always on” and capable of tolerating failures 
transparently. No system shutdown was required to replace failed components, and the system could work 
without interruption. Now their popularity and deployments have reduced, but evolved versions of such 
systems are still in use for transaction processing (such as online banking, airline ticket booking, 
supermarket and telcos, and government services).  
1.9.3 Clusters. Cluster computing started as a low -cost alternative to the use of mainframes and 
supercomputers. The technology advancement that created faster and more powerful mainframes and 
supercomputers eventually generated an increased availability of cheap commodity machines as a side 
effect. These machines could then be connected by a high -bandwidth networkand controlled by specific 
software  tools  that manage  them  as a single  system.  Built  by commodity  machines,  they were  cheaper  than 
mainframes and made high -performance computing available to a large number of groups, including 
universities and small research labs. Moreover, clusters could be easily extended if more computational 
power was required.  1.9.4 Grids.  Grid computing  appeared  in the early  1990s  as an evolution  of cluster  computing.  In an analogy 
to the power grid, grid computing proposed a new approach to access large computational power, huge 
storage facilities, and a variety of services. Users can “consume” resources in the same way as they use 
other utilities such as power, gas, and water. Grids initiallydeveloped as aggregations of geographically 
dispersed  clusters  by means  of Internet connections.These clusters  belonged  to different  organizations,  and 
arrangements were made among them to share the computational power. Several developments made 
possible  the diffusion  of computing grids:  (a) clusters  became  quite  common  resources;  (b) they were  often 
underutilized; (c) new problems were requiring computational power that went beyond the capability of 
single clusters; and (d) the improvements in networking and the diffusion of the Internet made possible 
long- distance,  high-bandwidth  connectivity.  All these  elements  led to the development  of grids,  whichnow 
serve a multitude of users across the world.  
 
1.9.5 Virtualization  
Virtualization is another core technology for cloud computing. It encompasses a collection of solutions 
allowing the abstraction of some of the fundamental elements for computing, such as hardware, runtime 
environments, storage, and networking. Today virtualization has become a fundamental element of cloud 
computing. Virtualization confers that degree of customization and control that makes cloud computing 
appealing for  users  and, at the same  time,  sustainablefor cloud services providers.  
Virtualization is essentially a technology that allows creation of different computing environments. These 
environments are called virtual because they simulate the interface that is expected by a guest. The most 
common example of virtualization is hardware virtualization . This technology allows simulating the 
hardware interface expected by an operating system. Hardware virtualization allows the coexistence of 
different software stacks on top of the same hardware. These stacks are contained inside virtual machine 
instances , which  operate in  complete  isolation  from  each other.  High -performance  servers  can host several 
virtual machine instances, thus creating the opportunity to have a customized software stack on demand. 
This is the base technology that enables cloud computing solutions to deliver virtual servers on demand, 
such as Amazon EC2, RightScale, VMware vCloud, and others. Together with hardware virtualization, 
storage  and network  virtualization  complete  the range  of technologies  for the emulation  of IT infrastructure. 
Virtualization technologies are also used to replicate runtime environments for programs.  
 
1.9.6 Web  2.0 
The Web  is the primary  interface  through  which  cloud  computing  delivers  its services.  At present,  the Web 
encompasses a  set of technologies  and services  that facilitate  interactiveinformation  sharing,  collaboration, 
user-centered design, and application composition. This evolution has transformed the Web into a rich 
platform for application development and is known as Web 2.0. This term captures a new way in which 
developers architect applications and  deliver  services  through  the Internet  and provides  new experience  for users  of these  applications and services.  
 
Web  2.0 brings  interactivity  and flexibility  into Web  pages,  providing  enhanced  user experience  by gaining 
Web -based  access  to all the functions  that are normally  found  in desktop  applications.These  capabilities  are 
obtained by integrating a collection of standards and technologies such as XML , Asynchronous JavaScript 
and XML (AJAX) , Web Services , and others.  
 
1.9.7  Service -oriented  computing  
Service orientation is the core reference model for cloud computing systems. This approach adopts the 
concept of services as the main building blocks of application and system development. Service -oriented 
computing (SOC) supports the development of rapid, low -cost, flexible, interoperable, and evolvable 
applications and systems.  
A service  is an abstraction  representing  a self-describing  and platform -agnostic  component  that can perform 
any function anything from a simple function to a complex business process.Virtually any piece of code 
that performs  a task can be turned  into a service  and expose  its functionalities  through  a network -accessible 
protocol. A service is supposed to be loosely coupled , reusable , programming language independent , and 
location transparent . Services are composed and aggregated into a service -oriented architecture (SOA). 
Service -oriented  computing  introduces  and diffuses  two important  concepts,  which  are also fundamental  to 
cloud computing: quality of service (QoS) and Software -as-a-Service (SaaS) . 
Quality of service (QoS) identifies a set of functional and nonfunctional attributes that can be used to 
evaluate  the behavior  of a service  from  different  perspectives. These  could be  performance  metrics  such as 
response time, or security attributes, transactional integrity, reliability, scalability, and availability. QoS 
requirements are established between the client and the provider via an SLA that identifies the minimum 
values (or an acceptable range) for the QoS attributes that need to be satisfied upon the service call.  
The concept  of Software -as-a-Service  introduces  a new delivery  model  for applications.  The term has been 
inherited  from  the world  of application  service  providers  (ASPs),  which  deliver  
software services -based solutions across the wide area network from a central datacenter and make them 
available on a subscription or rental basis.  
 
1.9.8 Utility -oriented  computing  
Utility computing is a vision of computing that defines a service -provisioning model for compute services 
in which resources such as storage, compute power, applications, and infrastructure are packaged and 
offered on a pay -per-use basis. The idea of providing computing as a utility like natural gas, water, power, 
and telephone connection has a long history but has become a reality today with the advent of cloud 
computing.  1.10 Building  Cloud  Computing  Environments  
The creation of cloud computing environments encompasses both the development of applications and 
systems that leverage cloud computing solutions and the creation of frameworks, platforms, and 
infrastructures delivering cloud computing services.  
Application  development  
Applications that leverage cloud computing benefit from its capability to dynamically scale on demand. 
One class  of applications that  takes the  biggest  advantage  of this feature  is that  of Web applications . These 
applications are characterized by complex processes that are triggered by the interaction with users and 
develop through the interaction between several tiers behind the Web front end.  
Another class of applications that can potentially gain considerable advantage by leveraging cloud 
computing is represented by resource -intensive applications . These can be either data - intensive or 
compute -intensive applications. In both cases, considerable amounts of resources are required to complete 
execution in a reasonable timeframe. It is worth noticing that these large amounts of resources are not 
needed constantly or for a long duration.  
 
Infrastructure  and system  development  
Distributed  computing,  virtualization,  service  orientation,  and Web  2.0 form  the core technologies  enabling 
the provisioning of cloud services from anywhere on the globe. Developing applications and systems that 
leverage the cloud requires knowledge across all these technologies.  
Infrastructure -as-a-Service solutions provide the capabilities to add and remove resources, but it is up to 
those who deploy systems on this scalable infrastructure to make use of such opportunities with wisdom 
and effectiveness. Platform -as-a-Service  solutions embed  into their  core offering  algorithms and rules that 
control the provisioning process and the lease of resources. These can be either completely transparent to 
developers or subject to fine control. Web 2.0 technologies constitute the interface through which cloud 
computing services are delivered, managed, and provisioned. Besides the interaction with rich interfaces 
through  the Web  browser,  Web  services  have  become  the primary  access  point  to cloud  computing  systems 
from  a programmatic  standpoint.  Service  orientation  is the underlying  paradigm  that defines  thearchitecture 
of a cloud computing system.  
Virtualization is another element that plays a fundamental role in cloud computing. This technology is a 
core feature of the infrastructure used by cloud providers.  
1.11 Computing  Platforms  and Technologies  
Amazon  web services  (AWS)  
AWS offers comprehensive cloud IaaS services ranging from virtual compute, storage, and networking to 
complete computing stacks. AWS is mostly known for its compute and storage - on- demand services, 
namely Elastic Compute Cloud (EC2) and Simple Storage Service (S3) . EC2 provides  users with  customizable  virtual hardware  that can be  used as the  base infrastructure for  deploying computing systems 
on the cloud.  It is possible  to choose  from  a large  variety  of virtual  hardware  configurations,  including  GPU 
and cluster instances. S3 is organized into buckets; these are containers of objects that are stored in binary 
form.  Users  can store  objects  of any size, from  simple  files to entire  disk images,  and have  them  accessible 
from everywhere.  
Google  AppEngine  
Google AppEngine is a scalable runtime environment mostly devoted to executing Web applications. 
AppEngine provides both a secure execution environment and a collection of services that simplify the 
development of scalable and high -performance Web applications. These services include in -memory 
caching, scalable data store, job queues, messaging, andcron tasks. Developers can build and test 
applications  on their own machines  using  the AppEngine  software  development  kit (SDK),  which  replicates 
the production  runtime  environment  and helps  test and profile  applications.  Once  development  is complete, 
developerscan  easily  migrate  their application  to AppEngine,  and make  the application  available  to the 
world.  The languages  currently  supported  are Python, Java.  
 
Microsoft Azure  
Microsoft Azure is a cloud operating system and a platform for developing applications in the cloud. It 
provides a scalable runtime environment for Web applications and distributed applications in general. 
Applications in Azure are organized around the concept of roles.Currently, there are three types of role: 
Web role , worker role , and virtual machine role . The Web role is designed to host a Web application, the 
worker role is a more generic container of applications and can be used to perform workload processing, 
and the virtual machine role provides a virtual environment in which the computing stack can be fully 
customized, includingthe operating systems.  
Hadoop  
Apache Hadoop is an open -source framework that is suited for processing large data sets on commodity 
hardware.  Yahoo!,  the sponsor  of the Apache  Hadoop  project,  has put considerable effort  into transforming 
the project into an enterprise -ready cloud computing platform for data processing. Hadoop is an integral 
part of the Yahoo!  cloud infrastructure  and supports several business processes  of the company.  Currently, 
Yahoo! manages the largest Hadoop cluster inthe world.  
Force.com  and Salesforce.com  
Force.com is a cloud computing platform for developing social enterprise applications. Force.com allows 
developers to create applications by composing ready -to-use blocks; a complete set of components 
supporting all the  activities of  an enterprise  are available.  The Force.com platform  is completely hosted on 
the cloud and provides complete access to its functionalities and those implemented in the hosted 
applications through Web services technologies.  Manjrasoft  Aneka  
Manjrasoft Aneka is a cloud application platform for rapid creation of scalable applications and their 
deployment on various types of clouds in a seamless and elastic manner. It supports a collection of 
programming abstractions for developing applications and a distributed runtime environment that can be 
deployed  on heterogeneous  hardware  (clusters,  networked  desktop computers, and cloud resources).  
These  platforms  are key examples  of technologies available  for cloud  computing.  They  mostly  fall into the 
three major market segments identified in the reference model: Infrastructure -as-a- Service , Platform -as- 
a-Service , and Software -as-a-Service . 
1.12 Virtualization  
Virtualization is a large umbrella of technologies and concepts that are meant to provide an abstract 
environment —whether virtual hardware or an operating system —to run applications. The term 
virtualization is often synonymous with hardware virtualization , which plays a fundamental role in 
efficiently delivering Infrastructure -as-a-Service (IaaS) solutions for cloud computing. In fact, 
virtualization technologies available in many flavors by providing virtual environments at the operating 
system level, the programming language level, and the application level. Moreover, virtualization 
technologies  provide  a virtual  environment  for not only executingapplications  but also for storage,  memory, 
and networking.  
Virtualization technologies have gained renewed interested recently due to the confluence of several 
phenomena:  
Increased performance and computing capacity. Nowadays, the average end -user desktop PC is powerful 
enough  to meet  almost  all the needs  of everyday  computing,  with extra  capacity  that is rarely  used.  Almost 
all these  PCs have resources enough to host a virtual machine manager and execute a virtual machine with 
by far acceptable  performance.  The same  consideration  applies  to the high-end side of the PC market,  where 
supercomputers can provide immense compute power that can accommodate the execution of hundreds or 
thousands of virtual machines.  
Underutilized hardware and software resources. Hardware and software underutilization is occurring due 
to (1) increased performance and computing capacity, and (2) the effect of limited or sporadic use of 
resources. Computers today are so powerful that in most cases only a fraction of their capacity is used by 
an application or the system. Moreover, if we consider the IT infrastructure of an enterprise, many 
computers are only partially utilized whereas they could be used without interruption on a 24/7/365 basis. 
For example, desktop PCs mostly devoted to office automation tasks and used by administrative staff are 
only used during work hours, remaining completely unused overnight. Using these resources for other 
purposes after hours could improve the efficiency of the IT infrastructure. To transparently provide such a 
service,  it would  be necessary  to deploy  a completely  separate  environment,  which  can be achieved  through 
virtualization.  Lack  of space.  The continuous  need  for additional  capacity,  whether  storage  or compute  power,  makes  data 
centers grow quickly. Companies such as Google and Microsoft expand their infrastructures by building 
data centers as large as football fields that are able to host thousands of nodes. Although this is viable for 
IT giants, in most cases enterprises cannot afford to build another data center to accommodate additional 
resource capacity. This condition, along with hardware underutilization, has led to the diffusion of a 
technique called server consolidation , for which virtualization technologies are fundamental.  
Greening  initiatives.  Recently,  companies  are increasingly  looking  for ways  to reduce  the amount  of energy 
they consume and to reduce their carbon footprint. Data centers are one of the major power consumers; 
Maintaining a  data center operation not only involves keeping servers  on, but a  great deal of  energy is also 
consumed  in keeping  them  cool.  Infrastructures  for cooling  have  a significant  impact  on the carbon  footprint 
of a data center.  Hence, reducing the  number  of servers  through  server consolidation will definitely reduce 
the impact of cooling and power consumption of a data center. Virtualization technologies can provide an 
efficient way of consolidating servers.  
Rise of administrative costs. The increased demand for additional capacity, which translatesinto more 
servers  in a data center,  is also responsible  for a significant  increment  in administrative  costs.  Computers — 
in particular, servers —do not operate all on their own, but they require care and feeding from system 
administrators. Common system administration tasks include hardware monitoring, defective hardware 
replacement,  server  setup and  updates,  server  resources  monitoring,  and backups.  These  are labor -intensive 
operations, and the higher the number of servers that have to be managed, the higher the administrative 
costs.  Virtualization  can help reduce  the number  of required  servers  for a given  workload,  thus reducing  the 
cost of the administrative personnel.  
1.13 Characteristics  of Virtualized  Environments  
Virtualization is a broad concept that refers to the creation of a virtual version of something, whether 
hardware,  a software  environment,  storage,  or a network.  In a virtualized  environment  there  are three  major 
components:  guest , host, and virtualization  layer . The guest  represents  the system  component  that interacts 
with the virtualization layer rather thanwith the host, as would normally happen. The host represents the 
original  environment  where  the guest  is supposed  to be managed.  The virtualization  layer  is responsible  for 
recreating the same or a different environment where the guest will operate. The Characteristics of 
Virtualization is as follows  
Increased security: The ability to control the execution of a guest in a completely transparent manner 
opens new possibilities for delivering a secure, controlled execution environment. The virtual machine 
represents an emulatedenvironment in which the guest is executed. All the operations of the guest are 
generally performed against the virtual machine, which then translates and applies them to the host. 
Resources exposed by the host can then be hidden or simply protected from the guest. Sensitive 
information that is containedin  the host can be naturally  hidden  without  the need  to install  complex  security  Guest  
Virtual  Image  
 Applications  
 Applications  
Virtual  Hardware  
 Virtual  
 Virtual  
Virtualization  
Software  Emulation  
Physical  Hardware  Physical  
 Physical  Networking  
Virtual  
Sharing  
 Aggregation  
 Emulation  
 Isolation  
 Virtualization  
Physical  policies.  
 
 
Figure  1.3: The virtualization  Reference  Model.  
Managed execution: Virtualization of the execution environment not  only allows increased security, but  
a wider range of features also can be implemented. In particular, sharing , aggregation , emulation , and 
isolation are the most relevant features  
 
Figure  1.4: Functions enabled  by managed  execution  
 
Aggregation.  Not only is it possible  to share  physical  resource  among several  guests,  but virtualization  also 
allows aggregation, which is the opposite process. A group of separate hosts can be tied together and 
represented to guests as a single virtual host. This function is naturally implemented in middleware for 
distributed computing, with a classic example represented by cluster management software, which 
harnesses the physical resources of a homogeneousgroup of machines and represents them as a single 
resource.  
Emulation.  Guest  programs  are executed  within  an environment  that is controlledby  the virtualization  layer,  which ultimately is a program. This allows for controlling and tuning the environment that is exposed to 
guests. For instance, a completely different environment with respect to the host can be emulated, thus 
allowing the execution of guest programs requiring specific characteristics that are not present in the 
physical  host.  Hardware  virtualization  solutions  are able toprovide  virtual  hardware  and emulate  a particular 
kind of device such as Small Computer System Interface (SCSI) devices for file I/O, without the hosting 
machine having such hardware installed.  
Isolation. Virtualization allows providing guests —whether they are operating systems, applications, or 
other entities —with a completely separate environment,in which they are executed. The guest program 
performs its activity by interacting with an abstraction layer, which provides access to the underlying 
resources.  The virtual  machine  can filter  the activity  of the guest  and prevent  harmful  operations  against  the 
host.  
Portability:  The concept  of portability  applies  in different  ways  according  to the specific  type 
of virtualization considered. In the case of a hardware virtualization solution, the guest is 
packaged  into a virtual  image  that, in most  cases,  can be safely  moved  and executed  on top of 
different  virtual  machines.  Except  for the file size,  thishappens with  the same  simplicity  with 
which we can display a picture image in different computers. Virtual images are generally 
proprietary formats that require a specific virtual machine manager to be executed.  
1.14 Taxonomy  of Virtualization  Techniques  
Virtualization  covers  a wide  range  of emulation  techniques  that are applied  to different  areas of  computing. 
A classification of these techniques helps us better understand their characteristics and use. The first 
classification  discriminates  against  the service  or entity  that is being  emulated.  Virtualization  is mainly  used 
to emulate  execution  environments , storage , and networks . Among  these  categories,  execution  virtualization 
constitutes the oldest, most popular, and most developed area. In particular we can divide these execution 
virtualization techniques into two major categories by considering the type of host they require. Process - 
level techniques are implemented on top of an existing operating system, which has full control of the 
hardware. System -level techniques are implemented directly on hardware and do not require —or require a 
minimum of support from —an existing operating system. Within these two categories we can lis t various 
techniques  that offer  the guest  a different  type of virtual  computation  environment:  bare hardware,  operating 
system resources, low -levelprogramming language, and application libraries.   
Figure  1.5: A taxonomy of  Virtualization  Techniques  
 
1.15.1  Execution  virtualization  
Execution virtualization includes all techniques that aim to emulate an execution environment that is 
separate from the one hosting the virtualization layer. All these techniques concentrate their interest on 
providing support for the execution of programs, whether these are the operating system, a binary 
specification of a program compiled against an abstract machine model, or an application. Therefore, 
execution virtualization can be implemented directly on top of the hardware by the operating system, an 
application, or libraries dynamically or statically linked to an application image.  
 
Figure  1.6: A Machine  Reference  Model  
The application binary interface (ABI) separates the operating system layer from the applicationsand 
libraries, which are managed by the OS. ABI covers details such as low -level data types, alignment, and 
call conventions and defines a format for executable programs. System calls are defined at this level. This  
interface allows portability of applications and libraries across operating systems that implement the same 
ABI.  The highest  level  of abstraction  is represented  by the application  programming  interface  (API) , which 
interfaces applications to libraries and/orthe underlying operating system.  
The instruction  set exposed  by the hardware  has been  divided  into different  security  classes  that define  who 
can operate  with them.  The first distinction  can be made  between  privileged  and nonprivileged  instructions. 
Nonprivileged instructions are those instructions that can be used without interfering with other tasks 
because they do not access shared resources. This category contains, for example, all the floating, fixed - 
point, and arithmetic instructions. Privileged instructions are those that are executed under specific 
restrictions and are mostly used for sensitive operations, which expose ( behavior -sensitive ) or modify 
(control -sensitive ) the privileged state. For instance, behavior -sensitive instructions are those that operate 
on the I/O, whereas control -sensitive instructions alter the state of the CPU registers.  
A possible implementation features a hierarchy of privileges (see Figure 1.7) in the form of ring - based 
security:  Ring  0, Ring  1, Ring  2, and Ring  3; Ring  0 is in the most  privileged  level  andRing 3 in the 
least privileged  level.  Ring  0 is used by the kernel  of the OS, rings  1 and 2 are used by the OS-level  services, 
and Ring 3 is used by the user. Recent systems support only two levels,with Ring 0 for supervisor mode 
and Ring 3 for user mode.  
Figure  1.7: Security  Rings  and Privileged  mode  
 
All the current  systems  support  at least two different  execution  modes:  supervisor  mode  and usermode . The 
first mode denotes an execution mode in which all the instructions (privileged and nonprivileged) can be 
executed without any restriction. This mode, also called master mode or kernel mode , is generally used by 
the operating system (or the hypervisor) to perform sensitive operations on hardware level resources. In 
user mode, there are restrictions to control the machine -level resources. If code running in user mode 
invokes the privileged instructions,hardware interrupts occur and trap the potentially harmful execution of 
the instruction. Conceptually, the hypervisor runs above the supervisor mode.  1.16 Hardware -level  Virtualization  
Hardware -level virtualization is a  virtualization technique  that provides an abstract execution environment 
in terms  of computer  hardware  on top of which  a guest  operating  system  can be run. In this model,  the guest 
is represented by the operating system, the host by the physical computerhardware, the virtual machine by 
its emulation, and the virtual machine manager by the hypervisor (see Figure 1.8). The hypervisor is 
generally  a program  or a combination  of software  and hardware  that allows  the abstraction  of the underlying 
physical hardware.  
Hardware -level  virtualization  is also called  system  virtualization , since  it provides  ISA to virtualmachines, 
which is the representation of the hardware interface of a system.  
Hypervisors : A fundamental element of hardware virtualization is the hypervisor, or virtualmachine 
manager (VMM).  
It recreates a hardware environment in which guest operating systems are installed. There aretwo major 
types of hypervisors: Type I and Type II . 
 
Figure  1.8: A hardware  virtualization  reference  model.  
Type I hypervisors run directly on top of the hardware. Therefore, they take theplace of the operating 
systems  and interact  directly  with the  ISA interface  exposed  by the underlying  hardware,  and they emulate 
this interface in order toallow  the management of guest operating systems. This type of hypervisor is also 
called a native virtual machine since it runs natively on hardware.  
Type  II hypervisors  require  the support  of an operating  system  to provide  virtualization  services.  This means 
that they are programs  managed  by the operating  system,  which  interact  with it through  the ABI and emulate 
the ISA of virtual hardware for guest operating systems. This type of hypervisor is also called a hosted 
virtual machine since it is hosted within an operating system.   
Figure  1.9: Hosted (left) and native  (right)  virtual  machines.  
 
A virtual machine manager is internally organized as described in Figure 1.10. Three main modules, 
dispatcher , allocator , and interpreter , coordinate  their activity  in order  to emulate  the underlying  hardware. 
The dispatcher constitutes the entry point of the monitor and reroutes the instructions issued by the virtual 
machine instance to one of the two other modules. The allocator is responsible for deciding the system 
resources to be provided to the VM: whenevera virtual machine tries to execute an instruction that results 
in changing  the machine  resources associated  with that  VM, the allocator is  invoked  by the dispatcher.  The 
interpreter  module  consists  of interpreter  routines.  These  are executed  whenever  a virtual  machine  executes 
aprivileged  instruction: a trap is triggered and the corresponding routine is executed.  
 
Figure  1.10:  A hypervisor  reference  architecture.  
 
Three  properties  of Virtual Machine  Manager  that have  to be satisfied:  
 
Equivalence. A guest running under the control of a virtual machine manager should exhibit the same 
behavior as when it is executed directly on the physical host.  
Resource  control.  The virtual machine manager  should  be in complete  control  of virtualized resources.  
VM VM VM VM 
ISA 
Virtual  Machine  Manager  
VM VM VM VM 
ABI 
 ISA 
Operative  System  
 Virtual  Machine  Manager  
ISA 
 ISA 
Hardware  
 Hardware  Efficiency. A statistically dominant fraction of the machine instructions should be executed without 
intervention from the virtual machine  manager.  
Popek  and Goldberg  provided  a classification  of the instruction  set and proposed  three  theorems that  define 
the properties that hardware instructions need to satisfy in order to efficiently support virtualization  
THEOREM  1 
For any conventional third -generation computer, a VMM may be constructed if the set of sensitive 
instructions for that computer is a subset of the set of privileged  instructions.  
This theorem establishes that all the instructions that change the configuration of the system resources 
should  generate  a trap in user mode  and be executed  under  the control  of the virtual machine  manager.  This 
allows hypervisors to efficiently control only those instructions that would reveal the presence of an 
abstraction layer while executing all the rest of the instructions without considerable performance loss.  
THEOREM  2 
A conventional  third -generation  computer  is recursively  virtualizable  if: 
✓ It is virtualizable  and 
✓ A VMM  without  any timing  dependencies  can be constructed  for it. 
Recursive virtualization is the ability to run a virtual machine manager on top of another virtualmachine 
manager. This allows nesting hypervisors as long as the capacity of the underlying resources can 
accommodate that. Virtualizable hardware is a prerequisite to recursive virtualization.  
THEOREM  3 
A hybrid VMM may be constructed for any conventional third -generation machine in which the set 
of user -sensitive instructions is a subset of the set of privileged instructions.  
There is another term, hybrid virtual machine (HVM) , which is less efficient than the virtual machine 
system. In the case of an HVM, more instructions are interpreted rather than being executed directly. All 
instructions  in virtual  supervisor  mode  are interpreted.  Whenever  there  is an attempt  to execute a  behavior - 
sensitive or control -sensitive instruction, HVM controls the execution directly or gains the control via a 
trap. 
1.17 Hardware  Virtualization  Techniques  
Hardware -assisted virtualization. This term refers to a scenario in which the hardware provides 
architectural support for building a virtual machine manager able to run a guest operating system in 
complete  isolation.  This technique  was originally  introduced  in the IBM System/370.  At present, examples 
of hardware -assisted  virtualization  are the extensions  to the x86-64 bit architecture  introduced  with Intel VT 
(formerly known as Vanderpool ) and AMD V (formerly known as Pacifica ).. Products such as VMware 
Virtual  Platform,  introduced  in 1999  by VMware,  which  pioneered  the field of x86 virtualization,  were  based  on this technique.  After  2006,  Intel and AMD  introduced  processor  extensions,  and a wide  range 
of virtualization solutions took advantage of them : Kernel -based Virtual Machine (KVM), VirtualBox, 
Xen, VMware, Hyper -V, Sun xVM, Parallels, and others.  
Full virtualization . Full virtualization refers to the ability to run a program, most likely an operating 
system, directly on top of a virtual machine and  without any modification, as though it were run on the 
raw hardware. To make these possible, virtual machine managers are required to provide a complete 
emulation of the entire underlying hardware. The principaladvantage of full virtualization is complete 
isolation, which leads to enhanced security, ease of emulation of different  architectures, and coexistence 
of different systems on the same platform.A simple solution to achieve full virtualization is to provide a 
virtual environment for all the instructions, thus posing some limits on performance.  
Paravirtualization . This is a not -transparent  virtualization  solution  that allows implementing thin  
virtual machine  managers. Paravirtualization techniques  expose  a software interface  to the  virtual machine 
that is slightly modified from the host and, as a consequence, guests need to be modified. The aim of 
paravirtualization is to provide the capability to demand the execution of performance -critical operations 
directly on the host, thus preventingperformance losses that would otherwise be experienced in managed 
execution. This technique has been successfully used by Xen for providing virtualization solutions for 
Linux -based operating systems specifically ported to run on Xen hypervisors.  
Partial virtualization. Partial virtualization provides a partial emulation of the underlying hardware, thus 
not allowing the complete execution of the guest operating system in complete isolation. Partial 
virtualization  allows  many  applications  to run transparently,  but not all the features  of the operating  system 
can be supported, as happens with full virtualization. Partial virtualization was implemented on the 
experimental IBM M44/44X. Address space virtualizationis a common feature of contemporary operating 
systems.  
1.18 Operating  system -level  virtualization  
Operating system -level virtualization offers the opportunity to create different and separated execution 
environments for applications that are managed concurrently. Differently from hardware virtualization, 
there is no virtual machine manager or hypervisor, and the virtualizationis done within a single operating 
system,  where  the OS kernel  allows  for multiple  isolated  user space  instances.  The kernel  is also responsible 
for sharing the  system resources  among instances and for limiting the impact of instances on each other. 
A user space instance in general contains a proper view of the file system, which is completely isolated, 
and separate IP addresses, software configurations, and access to devices. Operating system -level 
virtualization aims to provide separated and multiple execution containers for running applications. 
Compared to hardware virtualization, this strategy imposes little or no overhead because applications 
directly use OS system calls and there is no need for emulation.  
Examples  of operating  system -level  virtualizations  are FreeBSD  Jails,  IBM  Logical  Partition  (LPAR),  SolarisZones and Containers, Parallels Virtuozzo Containers, OpenVZ, iCore Virtual Accounts, Free 
Virtual Private Server (FreeVPS).  
1.19 Programming  language -level  virtualization  
Programming language -level virtualization is mostly used to achieve ease of deployment of applications, 
managed execution, and portability across different platforms and operating sys - tems. It consists of a 
virtual machine executing the byte code of a program, which is the resultof the compilation process. 
Compilers  implemented  and used this technology  to produce  a binaryformat  representing  the machine  code 
for an abstract architecture. The characteristics of this architecture vary from implementation to 
implementation.  
Programming  language -level  virtualization  has a long trail in computer  science  history  and orig- inally  was 
used in 1966 for the implementation of Basic Combined Programming Language (BCPL), a language for 
writing compilers and one of the ancestors of the C programming language. Other important examples of 
the use of this technology have been the UCSD Pascal and Smalltalk. Virtual machine programming 
languages become popular again with Sun’s introduction of the Java platform in 1996.  
Currently, the Java platform and .NET Framework represent the most popular technologies for enterprise 
application development. The main advantage of programming -level virtual machines,also called process 
virtual machines , is the ability to provide a uniform execution environment across different platforms. 
Programs  compiled  into byte code  can be executed  on any operating  system  and platform  for which  a virtual 
machine able to execute that code has been provided.  
1.20 Application -level  Virtualization  
Application -level  virtualization  is a technique allowing  applications  to be run in runtime  environments  that 
do not natively support all the features required by such applications. In this scenario, applications are not 
installed in the expected runtime environment but are run  as though they were. In general, these 
techniques are mostly concerned with partial file systems, libraries, and operating system component 
emulation. Such emulation is performed by a thin layer —a program or an operating system component — 
that is in charge of executing the application. Emulation can also be used to execute program binaries 
compiled for different hardware architectures. In this case, one of the following strategies can be 
implemented:  
• Interpretation. In this technique every source instruction is interpreted by an emulator for executing 
native ISA instructions, leading to poor performance. Interpretation has a minimal startup cost but a huge 
overhead, since each instruction is emulated.  
• Binary translation. In this technique every source instruction is converted to native instructions with 
equivalent functions. After a block of instructions is translated, it is cached and reused. Binary translation 
has a large  initial  overhead  cost, but over time it is subject  to better  performance,  since  previously  translated  instruction  blocks  are directly  executed.  
Application virtualization is a good solution in the case of missing libraries in the host operating system. 
One of the most popular solutions implementing application virtualization is Wine, which is a software 
application allowing Unix -like operating systems to execute programs written for the Microsoft Windows 
platform  
1.21 Other  Types  of Virtualizations  
1. Storage  virtualization  
Storage virtualization is a system administration practice that allows decoupling the physical organization 
of the hardware  from  its logical  representation.  Using  this technique,  users  do not have  to be worried about 
the specific  location  of their data,  which  can be identified  using  a logical  path.  There  are different  techniques 
for storage virtualization, one of the most popular being network -based virtualization by means of storage 
area networks (SANs) . 
2. Network  virtualization  
Network virtualization combines hardware appliances and specific software for the creation and 
management of a virtual network. Network virtualization can aggregate different physicalnetworks into a 
single  logical  network  (external  network  virtualization)  or provide  network -likefunctionality  to an operating 
system  partition  (internal  network  virtualization).  The result of  external  network  virtualization  is generally 
a virtual LAN (VLAN) . A VLAN is an aggregation of hosts that communicate with each other as though 
they were located under the same  
broadcasting  domain.  There  are several  options  for implementing  internal  network  virtualization:  The guest 
can share the same net - work interface of the host and use Network Address Translation (NAT) to access 
the network; the virtual machine manager can emulate, and install on the host, an additional network 
device, together with the driver; or the guest can have a private network only with the guest.  
3. Desktop  virtualization  
Desktop virtualization abstracts the desktop environment available on a personal computer in order to 
provide access to it using a client/server approach. Desktop virtualization provides the same out - come of 
hardware virtualization but serves a different purpose. Similarly to hardware virtualization, desktop 
virtualization makes accessible a different system as though it were natively installed on the host, but this 
system  is remotely  stored  on a different  host and accessed  through  a network  connection.  Moreover,  desktop 
virtualization  addresses  the problem  of making  the same  desktop  environment  accessible  from  everywhere. 
The advantages of desktop virtualization are high availability, persistence, accessibility, and ease of 
management. Infrastructures for desktop virtua - lization based on cloud computing solutions include Sun 
Virtual Desktop Infrastructure (VDI), Parallels Virtual Desktop Infrastructure(VDI), Citrix XenDesktop, 
and others.  4. Application  server  virtualization  
Application  server  virtualization  abstracts  a collection  of application  servers  that provide  the same  services 
as a single virtual application server by using load -balancing strategies and providing a high -availability 
infrastructure for the services hosted in the application server. This is a particular form of virtualization 
and serves the same purpose of storage virtualization: providing a better quality of service rather than 
emulating a different environment.  
1.22 Virtualization  and Cloud  Computing  
Virtualization plays an important role in cloud computing since it allows for the appropriate degree of 
customization, security, isolation, and manageability that are fundamental for delivering IT services on 
demand. Virtualization technologies are primarily used to offer configurable computing environments and 
storage.  
Particularly  important  is the role of virtual  computing  environment  and execution  virtualization  techniques.  
Among  these,  hardware  and programming  language  virtualization  are the techniques  
adopted in cloud computing systems. Hardware virtualization is an enabling factor for solutions in the 
infrastructure -as-a-Service (IaaS) market segment, while programming language virtualization is a 
technology leveraged in Platform -as-a-Service (PaaS) offerings. In both cases, the capability of offering a 
customizable and sandboxed environment constituted anattractive business opportunity for companies 
featuring a large computing infrastructure that wasable to sustain and process huge workloads. Moreover, 
virtualization also allows isolation and a finer control, thus simplifying the leasing of services and their 
accountability on the vendor side.  
Virtualization allows us to create isolated and controllable environments, it is possible to serve these 
environments with the  same  resource without them interfering with each other. If the  underlying resources 
are capable enough, there will be no evidence of such sharing. It allows reducing the number of active 
resources by aggregating virtual machines over a smaller number of resources that become fully utilized. 
This practice is also known as server consolidation, whilethe movement of virtual machine instances is 
called virtual machine migration (see Figure 3.10). Because virtual machine instances are controllable 
environments, consolidation can be applied with a minimum impact, either by temporarily stopping its 
execution  and moving  its data to the new resources  or by performing  a finer  control  and moving  the instance 
while it is running. This second techniques is known as live migration and in general is more complex to 
implement but more efficient since there is no disruption of the activity of the virtual machine instance  
Pros  and cons  of virtualization  
 
1.22. 1 Advantages  of virtualization  
 
Managed  execution  and isolation  are perhaps  the most  important advantages  of virtualization.  Inthe  case of 
techniques supporting the creation of virtualized execution environments, these two characteristics  allow  building secure and controllable computing environments. A virtual execution environment can be 
configured as a sandbox, thus preventing any harmful operation tocross the borders of the virtual host. 
Moreover, allocation of resources and their partitioning among different guests is simplified, being the 
virtual host controlled by a program. This enables fine -tuning of resources, which is very important in a 
server consolidation scenario and is also a requirement for effective quality of service  
Portability and self -containment also contribute to reducing the costs of maintenance, since the number of 
hosts is  expected  to be  lower  than the number  of virtual machine  instances. By means of  virtualization it  is 
possible to achieve a more efficient use of resources. Multiple systems can securely coexist and share the 
resources of the underlying host, without interfering with each other.  
1.22.2  Performance  degradation  
 
Performance is definitely one of the major concerns in using virtualization technology. Since virtulization 
interposes  an abstraction  layer  between  the guest  and the host,  the guest  can experience  increased  latencies. 
For instance,  in the case  of hardware  virtualization,  where  the intermediate emulates  a bare machine on  top 
of which an entire system can be installed, the causes of performance degradation  can be traced back to 
the overhead introduced by the following  activities:  
✓ Maintaining  the status of  virtual processors  
 
✓ Support  of privileged  instructions  (trap  and simulate  privileged  instructions)  
✓ Support  of paging  within  VM 
 
1.22.3  Console  functions  
Furthermore, when hardware virtualization is realized through a program that is installed or exe - cuted on 
top of the host operating systems, a major source of performance degradation is repre - sented by the fact 
that the virtual machine manager is executed and scheduled together with otherapplications, thus sharing 
with them the resources of the  host.  
Similar  consideration  can be made  in the case of virtualization  technologies  at higher  levels,such  as in 
the case of programming language virtual machines (Java, .NET, and others). Binary translation and 
interpretation can slow down the execution of managed applications. Moreover, because their execution is 
filtered  by the runtime  environment,  access  to memory  and other  physi - cal resources  can represent  sources 
of performance  degradation.  
These concerns are becoming less and less important thanks to technology advancements andthe ever - 
increasing computational power available today. For example, specific techniques for hard - ware 
virtualization such as paravirtualization can increase the performance of the guest program by offloading 
most of its execution to the host without any change. In programming - level virtual machines such  as the  JVM  or .NET, compilation to native  code  is offered as  an option when  perfor - mance  is a serious  concern.  
1.22.4  Disadvantages:  
 
Inefficiency  and degraded  user experience  
 
Virtualization  can sometime  lead to an inefficient  use of the host.  In particular,  some  of the specific  features 
of the host cannot  be exposed  by the abstraction  layer  and then becomeinaccessible.  In the case of hardware 
virtualization, this could happen for device drivers: The virtual machine can sometime simply provide a 
default  graphic  card that maps  only a subset  of the features  available  in the host.  In the case of programming - 
level virtual machines, some of thefeatures of the underlying operating systems may become inaccessible 
unless specific libraries are used.  
Security  holes  and new threats  
 
Virtualization  opens  the door to a new and unexpected  form  of phishing.  The capability  of emulating  a host 
in a completely  transparent  manner  led the way to malicious  programs that  are designed  to extract  sensitive 
information from the guest.  
In the case of hardware virtualization, malicious programs can preload themselves before the operating 
system  and act as a thin virtual  machine  manager  toward  it. The operating  system  is then controlled  and can 
be manipulated to extract sensitive information of interest to  third parties.  
Technology  examples  
 
1.23 Xen:  paravirtualization  
 
Xen is an open -source  initiative  implementing  a virtualization  platform  based  on paravirtualization.  Initially 
developed  by a group  of researchers  at the University  of Cambridgein  the United  Kingdom,  Xen now has 
a large  open -source  community  backing  it. . Xen -based  technology  is used for either  desktop  virtualization 
or server virtualization, and recently it has also been used to provide cloud computing solutions by means 
of Xen Cloud Platform (XCP).  
Figure 1.11 describes the architecture of Xen and its mapping onto a classic x86 privilege model. A Xen - 
based  system  is managed  by the Xen hypervisor,  which  runs in the highest  
privileged  mode and  controls the  access of  guest  operating  system  to the underlying hardware.  
Guest operating systems are executed within domains, which represent virtual machine instances. 
Moreover,  specific  control  software, which  has privileged  access  to the host and controls  all the other  guest 
operating  systems,  is executed  in a special  domain called  Domain  0.This  is the  first one that is loaded  once 
the virtual machine manager has completely booted, andit hosts a HyperText  Transfer Protocol (HTTP) 
server that serves requests for virtual machine creation, con - figuration, and termination. This component  constitutes  the embryonic  version  of adistributed  virtual  machine  manager,  which  is an essential  component 
of cloud computing systems providing Infrastructure -as-a-Service (IaaS) solutions.  
 
 
Figure  1.11 Xen architecture  and guest  OS management  
Many of the x86 implementations support four different security levels, called rings, whereRing 0 
represent the level with the highest privileges and Ring 3 the level with the lowest ones.  
Because  of the structure  of the x86 instruction  set, some  instructions  allow  code  executing  in Ring  3 to jump 
into Ring 0 (kernel mode). Such operation is performed at the hardware level and therefore within a 
virtualized environment will result in a trap or silent fault, thus preventing  
the normal operations of the guest operating system, since this is now running in Ring 1.This condition is 
generally triggered by a subset of the system calls. To avoid this situation, operating systems need to be 
changed in their implementation, and the sensitive system calls need to be reimplemented with hypercalls, 
which are specific calls exposed by the virtual machine interface of Xen. With the use of hypercalls, the 
Xen hypervisor is able to catch the execution of all the sensitive instructions, manage them, and return the 
control to the guest operating system by means of a supplied handler.  
Paravirtualization  needs  the operating  system  codebase  to be modified,  and hence  not all operating  systems 
can be used as guests in a Xen -based environment. Open -source operating systems such as Linux can be 
easily  modified,  since  their code  is publicly available  and Xen provides  full support  for their virtualization, 
whereas components of the Windows family are generally not supported by Xen unless hardware -assisted 
virtualization is available.  
VMware:  full virtualization:  VMware’s  technology  is based  on the concept  of full virtualization , where  the underlying  hardware  is replicated  and made  available  to the guest  operating  system,  which  runs unaware 
of such abstraction layers and does not need to be modified. VMware implements full virtualization either 
in the desktop environment, by means of Type II hypervisors, or in the server environment, by means of 
Type I hypervisors. In both cases, full virtualization is made possible by means of direct execution (for no 
sensitive  instructions) and  binary  translation  (for sensitive  instructions),  thus allowing  the virtualization  of 
architecture such as  x86. 
1.24 Microsoft  Hyper -V 
To virtualize  hardware,  i.e. create  a hardware  environment  that does not have  a physical  form,  you need  an 
intermediary between the physical computer  and the  virtual machine.  This interface  is called a  hypervisor. 
The physical host system can be mapped to multiple virtual guest systems (child partitions) that share the 
host hardware (parent partition). Microsoft has created its own hypervisor, Hyper -V, which is included in 
the professional  versions of  Windows  10 or Windows  8. The software  is also  installed  in Windows  Server. 
Hyper -V gives Windows users the ability to start their own virtual machine . In this virtual machine, a 
complete  hardware  infrastructure  with RAM,  hard disk space, processor  power,  and other  components  can 
be virtualized. A separate operating system runs on this basis, which does not necessarily have to be 
Windows.  It is very popular,  for example,  to run an open -source  distribution  of Linux  in a virtual  machine. 
Virtualization  technology  can be used in different  situations  for different  needs.  Hyper -V is usually  used in 
test environments. In this context, virtualization has two advantages:  
1. Computer  environments  which  are otherwise  not accessible can be accessed . For example,  instead 
of setting  up your own PC with Linux,  you can easily  display  the Linux  operating  system  in a virtual 
machine.  
2. The virtual machine is self-contained . This means that if you run software that causes a system 
crash, the physical device is not at risk. Only the virtual machine would need to be reset.  
Private users can use Hyper -V, for example, if they want to use software that would not run under their 
current  version  of Windows - either  because  the program requires  an older  version  of the operating system 
or because only Linux is supported.  
Virtualization via Hyper -V is a great advantage for software developers in particular. Any program they 
create can be tested under a huge variety of software  and hardware conditions. In addition, due to the self - 
contained nature of the virtual machines, there is no need to worry about faulty code causing damage to 
their own systems.  
 
Microsoft  Hyper -V’s Architecture  
 
Hyper -V allows x64 versions of Windows to host one or more virtual machines, which in turn contain a 
fully configured operating system. These “child” systems are treated as partitions. The term is otherwise  known from hard disk partitioning - and Hyper -V virtualization works in a similar way. Each virtual 
machine is an isolated unit next to the “parent” partition, the actual operating system.  
The individual partitions are  orchestrated by the hypervisor. The subordinate partitions can be created and 
managed via an interface (Hypercall API) in the parent system. However, the isolation is always 
maintained. Child systems are assigned virtual hardware resources but can never access the physical 
hardware of the parent.  
To request  hardware  resources,  child  partitions  use VMBus.  This is a channel  that enables communication 
between partitions. Child systems can request resources from the parent, but theoretically they can also 
communicate with each other.  
The partitions  run services  that handle  the requests  and responses  that run over the VMBus.  The host system 
runs the Virtualization Service Provider (VSP), the subordinate partitions run the Virtualization Service 
Clients (VSC).  
 
 
Figure 1.13:  Microsoft  Hyper -V Architecture  
 
Differences  between  Hyper -V and other  virtualization techniques  
Unlike any other virtualization techniques, Hyper -V has the advantage of being integrated with Windows. 
Anyone using the Microsoft operating system for PCs or servers can benefit from this close integration. 
Hyper -V is a type 1 hypervisor, which is also something only  few other techniques offer.  This means  
that Hyper -V is based directly on the system hardware . Type 2 hypervisors, on the other hand, must 
always go through the parent operating system to provide resources.  
Advantages  
For Windows users, a very clear advantage is the close connection to the operating system. This can also 
mean a more cost-effective solution because Hyper -V is often included for free with Windows. Hyper -V 
can keep up with the competition in terms of its functionality. Users of Hyper -V can expect high 
performance, as long as they only work with Windows as a guest system. Since admin work is relatively 
simple, even beginners can benefit from virtualization via Hyper -V. 
Disadvantages  
Although Hyper -V works very well with Windows, the software reaches its limits with other operating 
systems. Hyper -V is not designed to run  on other  systems, and the  possible  guest  systems  are very limited. 
Apart  from  Windows,  only a few selected  Linux  distributions  can run in a virtual  machine.  For example,  if 
you want to use macOS as a guest system, you have to use an additional product. Unfortunately, a high 
loss of performance occurs when you run multiple Linux systems at once.  
 
Multiple  Choice  Questions  
1. What  is the fundamental concept  behind  Cloud Computing?  
a) Hardware  virtualization  
b) Internet  connectivity  
c) Distributed  systems  
d) Utility computing  
Answer:  b) Internet  connectivity  
2. Which  term is synonymous  with "on-demand,  self-service"  in Cloud  Computing?  
a) Utility computing  
b) Scalability  
c) Elasticity  
d) Virtualization 
Answer:  c) Elasticity  
3. Which  of the following is NOT  a characteristic of  Cloud Computing?  
a) Resource  pooling  
b) On-site data centers  
c) Rapid  elasticity  
d) Measured  service  
Answer:  b) On-site data centers  
4. Which  historical  development paved  the way for Cloud  Computing's  widespread  adoption?  
a) The invention of  the internet  
b) The creation  of the first computer  
c) The development of  distributed systems  d) The emergence of virtualization 
Answer:  a) The invention  of the internet  
5. What  is the primary  goal of  virtualization  in Cloud  Computing?  
a) To increase  hardware  costs  
b) To improve  network  security  
c) To reduce  hardware  and maintenance costs  
d) To enhance  user experience  
Answer:  c) To reduce  hardware  and maintenance  costs  
6. Which component of Cloud Computing provides a visual representation of the Cloud's structure and  
services?  
a) Cloud  service  provider  
b) Cloud  Computing  reference  model  
c) Cloud  architecture  diagram  
d) Cloud application developer 
Answer:  c) Cloud  architecture  diagram  
7. What  is the relationship  between  Service -Oriented  Computing  and Cloud  Computing?  
a) Service -Oriented  Computing  is a type of Cloud  Computing.  
b) Service -Oriented  Computing  and Cloud  Computing  are unrelated concepts.  
c) Cloud  Computing  is a type of Service -Oriented  Computing.  
d) Service -Oriented  Computing  and Cloud  Computing  are synonymous  terms. 
Answer: c) Cloud Computing is a type of Service -Oriented Computing.  
8. What  is the primary  advantage  of utility -oriented  computing  in Cloud  Computing?  
a) It focuses  on data storage  only.  
b) It allows  users  to pay only for  the resources  they consume.  
c) It provides  unlimited  resources  to all users.  
d) It eliminates  the need  for virtualization.  
Answer:  b) It allows  users to  pay only for the resources  they consume.  
9. Which  technology  is often  used to build  Cloud  Computing  environments  due to its flexibility  and 
scalability?  
a) Virtualization  
b) Distributed  systems  
c) Web  2.0 
d) Service -Oriented  Computing 
Answer: a) Virtualization  
10. Which  Cloud  service  provider  is known  for its Infrastructure  as a Service  (IaaS)  offerings,  such as EC2?  
a) Google  App Engine  b) Microsoft  Azure  
c) Amazon  Web  Services  (AWS)  
d) Hadoop  
Answer:  c) Amazon  Web  Services  (AWS)  
12. How  does elasticity  differ  from  scalability  in Cloud  Computing?  
a) Elasticity  is the ability  to scale  resources  automatically,  while  scalability  is the manual  process  of adding 
resources.  
b) Scalability  is the ability  to scale  resources  automatically,  while  elasticity  is the manual  process  of adding 
resources.  
c) Elasticity  and scalability  are synonymous  terms.  
d) Scalability  and elasticity  are unrelated  concepts  in Cloud  Computing.  
Answer:  a) Elasticity  is the ability  to scale  resources  automatically,  while  scalability  is the manual  process 
of adding resources.  
13. Which  Cloud  Computing  characteristic  allows  users  to access  services  without  requiring  human 
intervention from the service provider?  
a) On-demand  self-service  
b) Rapid  elasticity  
c) Resource  pooling  
d) Measured  service  
Answer:  a) On-demand  self-service  
14. What  is the role of a hypervisor  in virtualization  technology?  
a) Managing  cloud  security  
b) Providing  an interface for  users  to access  cloud  services  
c) Virtualizing  and managing  the underlying  hardware  
d) Developing  cloud  applications  
Answer:  c) Virtualizing and  managing  the underlying hardware  
15. How  does Para virtualization  differ  from  Full virtualization?  
a) Para virtualization  requires  no modification  of the guest  operating  system,  while  Full virtualization does.  
b) Full virtualization  requires  no modification  of the guest  operating  system,  while  Para virtualization  does.  
c) Para virtualization  is a type of cloud  architecture,  while  Full virtualization is  a security  protocol.  
d) Para virtualization and Full virtualization are unrelated concepts in Cloud Computing. 
Answer:  a) Para virtualization  requires  no modification  of the guest  operating  system,  while  Full 
virtualization does.  
16. In Cloud  Computing, what  is the main  purpose  of the Xen hypervisor?  
a) Managing  cloud  security  
b) Providing  an interface for  users  to access  cloud  services  c) Virtualizing  and managing  the underlying  hardware  
d) Developing  cloud  applications  
Answer:  c) Virtualizing and  managing  the underlying hardware  
17. What  are the potential  drawbacks of  relying  solely on  Cloud  Computing  without  on-site data centers?  
a) Reduced  scalability  and flexibility  
b) Increased  hardware  and maintenance  costs  
c) Dependency  on internet  connectivity  and service  providers  
d) Improved  data security  
Answer:  c) Dependency  on internet  connectivity and  service  providers  
18. Why  is virtualization considered a  key enabling  technology  for Cloud Computing?  
a) It reduces  the need  for internet  connectivity.  
b) It enables  the automatic  scaling  of resources.  
c) It eliminates  the need  for service -oriented  computing.  
d) It optimizes  data storage.  
Answer:  b) It enables  the automatic  scaling  of resources.  
19. Compare  and contrast  the characteristics  of virtualized  environments  and non-virtualized  environments 
in the context of Cloud Computing.  
a) Virtualized  environments  are more  secure  but less scalable.  
b) Non-virtualized  environments are  more  cost-effective  but less flexible.  
c) Virtualized  environments  provide  isolation  but may introduce  overhead.  
d) Non-virtualized  environments are  more  scalable  but less secure.  
Answer:  c) Virtualized  environments  provide  isolation but  may introduce overhead.  
20. Identify  the key advantages  of using  a utility -oriented  computing  model  in Cloud  Computing,  and 
explain how it benefits both service providers and consumers.  
a) Utility -oriented computing reduces costs for service providers and enhances service quality for 
consumers.  
b) Utility -oriented  computing  eliminates  the need for  virtualization  and increases  resource  pooling.  
c) Utility -oriented  computing improves  resource  isolation  for service  providers  and consumers.  
d) Utility -oriented  computing  simplifies  billing  for service  providers  and consumers.  
Answer:  a) Utility -oriented  computing  reduces  costs  for service  providers  and enhances  service  quality  for 
consumers.  
21. Analyze  the role  of distributed systems in Cloud Computing and provide  examples of how  distributed 
systems support the scalability and reliability of cloud services.  
a) Distributed  systems  enable  load balancing  and fault tolerance,  ensuring  high availability  of cloud 
services. Examples include content delivery networks (CDNs) and distributed databases.  
b) Distributed  systems  are unrelated  to Cloud  Computing  and have  no impact  on cloud  service  scalability  or reliability.  
c) Distributed systems focus solely on resource pooling and do not contribute to cloud service scalability 
or reliability.  
d) Distributed  systems  are primarily  responsible  for cloud  security  and data encryption.  
Answer:  a) Distributed systems  enable  load balancing  and fault tolerance,  ensuring  high availability  of 
cloud services. Examples include content delivery networks (CDNs) and distributed databases.  
22. Evaluate  the significance  of Web  2.0 in the context  of Cloud  Computing,  and discuss  how it has 
transformed user interactions with online services.  
a) Web  2.0 has made  Cloud Computing  obsolete  by introducing  new web technologies.  
b) Web 2.0 has enhanced user engagement and collaboration, making Cloud Computing more interactive 
and user -friendly.  
c) Web  2.0 has no relevance  to Cloud Computing,  as they are separate  concepts.  
d) Web  2.0 has increased  the complexity  of Cloud  Computing,  making  it less accessible  to users.  
Answer: b) Web 2.0 has  enhanced user engagement and collaboration, making Cloud Computing more  
interactive and user -friendly.  
23. Assess  the pros and cons of using  Microsoft  Hyper -V as a virtualization  solution  in a Cloud  Computing 
environment, and compare it to alternative virtualization technologies.  
a) Microsoft  Hyper -V offers  strong  security  but lacks  scalability  compared  to other  virtualization  solutions.  
b) Microsoft  Hyper -V excels  in scalability  but may have  security  vulnerabilities  compared  to other 
virtualization technologies.  
c) Microsoft  Hyper -V is not suitable  for Cloud  Computing due  to its limited features.  
d) Microsoft  Hyper -V is the most  cost-effective  virtualization solution  for Cloud  Computing.  
Answer:  b) Microsoft  Hyper -V excels  in scalability  but may have  security  vulnerabilities  compared  to other 
virtualization technologies.  
24. Which  statement  accurately differentiates  Amazon  Web  Services  (AWS)  from  Google  App Engine?  
a) AWS  offers  mainly  PaaS solutions,  while  Google  App Engine  focuses  on IaaS.  
b) AWS  targets  a broad  audience, while  Google  App Engine  caters  to startups.  
c) AWS  specializes  in serverless computing,  whereas Google  App Engine  emphasizes  containers.  
d) AWS  and Google  App Engine  have  similar  service  offerings.  
Answer:  a) AWS  offers mainly  PaaS solutions,  while  Google  App Engine focuses on  IaaS.  
25. Which  categorization  of virtualization  techniques  is correct?  
a) Hardware  Virtualization,  Software  Virtualization,  Network  Virtualization;  Hardware  Virtualization 
offers high performance.  
b) Server Virtualization, Storage Virtualization, Desktop Virtualization; Storage Virtualization optimizes 
resource use.  
c) Para virtualization,  Full virtualization,  Container -based  virtualization;  Full virtualization  provides  high isolation.  
d) Hardware  Virtualization,  Para virtualization,  OS-level  virtualization;  OS-level  virtualization  is 
compatible with various OSs.  
Answer: c)  Para virtualization, Full virtualization, Container -based virtualization; Full virtualization 
provides high isolation.  
Long  Answer  Questions  
 
1. Define  Cloud  Computing  and briefly  explain  examples  of such systems  exist  across  all market 
segments.  
2. Explain  Cloud  Computing  Reference  Model  
3. Explain  five core technologies  that played  an important  role in the  realization  of cloud computing.  
 
4. How  to build cloud Computing  environments? Explain.  
5. In your viewpoints list  and explain  various  Computing  Platforms and  Technologies.  
 
6. How  virtualization  is important  in cloud  computing.  Explain  briefly  various  characteristics  of 
virtualization.  
7. Explain  the taxonomy  of virtualization  with execution  virtualization.  
 
8. How  to achieve  hardware  level  virtualization?  Explain  
9. Explain  the 3 Theorems  of Hardware  level  virtualization.  
 
10. What do you understand about Operating system level, Programming Level, and application -level 
Virtualization?  
11. Explain  Xen-para virtualization  with a neat diagram.  
12. Explain  Microsoft  Hyper -V Virtualization.  
 
*********************  Error extracting images/OCR from PDF: Unable to get page count. Is poppler installed and in PATH?