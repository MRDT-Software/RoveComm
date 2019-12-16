#ifndef RoveEthernetTcp_h
#define RoveEthernetTcp_h

#include <stdint.h>
#include <stddef.h>
#include <Energia.h>
#include <Ethernet.h>

#include "RoveCommManifest.h"
#include "RoveCommPacket.h"

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class RoveCommEthernetTcp
{
  public:
    EthernetServer Server;

    struct rovecomm_packet read();

    /////begin/////////////////////////////////////////////////////////////////////////////////////////////////////////
    //Overloaded begin
	  //Default ip address = 192.168.1.XXX
    //For the purposes of TCP, the board is treated as the server, where Base Station is the client
	  void begin(uint8_t server_ip_octet, const int port);
    void begin(byte server_ip[4], const int port);

	  /////writeReliable////////////////////////////////////////////////////////////////////////
	  //Single-value writeReliable
	  //Overloaded for each data type
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const uint8_t  data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const uint16_t data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const uint32_t data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const int8_t   data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const int16_t  data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const int32_t  data);

    //Array entry writeReliable
	  //Overloaded for each data type
    void writeReliable(const uint16_t data_id, const int     data_count, const int      *data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const uint8_t  *data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const uint16_t *data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const uint32_t *data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const int8_t   *data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const int16_t  *data);
    void writeReliable(const uint16_t data_id, const uint8_t data_count, const int32_t  *data);
  
  private:
    //Called by overloaded writeReliable functions
    void _writeReliable(  const uint8_t  data_type_length, const roveware::data_type_t data_type, 
                          const uint16_t data_id,    const uint8_t data_count, const void* data);
};

#endif // RoveCommEthernetTcp_h