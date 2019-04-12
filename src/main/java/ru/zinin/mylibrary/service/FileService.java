package ru.zinin.mylibrary.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service
public class FileService {

    @Value("${upload.path}")
    private String uploadPath;

    public String extractPicture(String filename) {
        if (!filename.endsWith(".fb2")) {
            return null;
        }
        Stream<String> files = null;
        try {
            files = Files.lines(Paths.get(uploadPath + "/" + filename)).filter(a -> a.contains("binary")).map(this::cut);
        } catch (IOException e) {
            e.printStackTrace();
        }
//        if (files)
        List<String> collect = files.collect(Collectors.toList());

//        System.out.println(collect.size());
        return collect.get(0);
    }

    private String cut(String s) {
        int start = s.indexOf("binary");
        int stop = s.lastIndexOf("binary");
        String result = s.substring(start, stop);
        start = result.indexOf(">");
        stop = result.lastIndexOf("<");
        result = result.substring(start + 1, stop);
        return result;

    }

    public String[] bookProp(String filename) {
        String[] prop = new String[4];
        try {

            DocumentBuilder documentBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
            Document document = documentBuilder.parse(uploadPath + "/" + filename);
            NodeList firstName = document.getElementsByTagName("first-name");
            NodeList lastName = document.getElementsByTagName("last-name");
            NodeList bookTitle = document.getElementsByTagName("book-title");
            NodeList annotation = document.getElementsByTagName("annotation");

            prop[0] = firstName.item(0) == null ? null : firstName.item(0).getTextContent();
            prop[1] = lastName.item(0) == null ? null : lastName.item(0).getTextContent();
            prop[2] = bookTitle.item(0) == null ? null : bookTitle.item(0).getTextContent();
            prop[3] = annotation.item(0) == null ? null : annotation.item(0).getTextContent();

        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        } catch (SAXException e) {
//            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return prop;
    }
}