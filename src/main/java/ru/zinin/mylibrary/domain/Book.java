package ru.zinin.mylibrary.domain;

import javax.persistence.*;

@Entity
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private String bookname;
    private String author;

    private String filename;

    @Column(name = "pic_name")
    private String pictureName;

    @Transient
    private String annotation="No annotations";


    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "user_id")
    private User reliser;

    public Book(String bookname, String author, User user) {
        this.bookname = bookname;
        this.author = author;
        this.reliser = user;
    }

    public Book() {
    }

    public User getReliser() {
        return reliser;
    }

    public void setReliser(User reliser) {
        this.reliser = reliser;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getBookname() {
        return bookname;
    }

    public void setBookname(String bookname) {
        this.bookname = bookname;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getPictureName() {
        return pictureName;
    }

    public void setPictureName(String pictureName) {
        this.pictureName = pictureName;
    }

    public String getAnnotation() {
        return annotation;
    }

    public void setAnnotation(String annotation) {
        this.annotation = annotation;
    }
}
