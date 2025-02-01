package org.levaldo.snapscrap

import com.google.cloud.functions.CloudEventsFunction
import com.google.gson.{JsonObject, JsonParser}
import io.cloudevents.CloudEvent
import java.util.{Base64, logging}
import java.nio.charset.StandardCharsets

class PubsubFunction extends CloudEventsFunction {
  private val logger = logging.Logger.getLogger(getClass.getName)

  override def accept(event: CloudEvent): Unit = {
    // Parse the CloudEvent data as JSON
    val eventData = new String(event.getData.toBytes, StandardCharsets.UTF_8)
    val jsonObject = JsonParser.parseString(eventData).getAsJsonObject
    val message = jsonObject.getAsJsonObject("message")
    
    // Get the base64 encoded data
    val encodedData = message.get("data").getAsString
    
    // Decode the base64 message data
    val decodedMessage = new String(
      Base64.getDecoder.decode(encodedData),
      StandardCharsets.UTF_8
    )

    // Log the message
    logger.info(s"Pub/Sub message: $decodedMessage")
  }
}
