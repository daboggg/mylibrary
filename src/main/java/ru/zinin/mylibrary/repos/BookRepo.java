package ru.zinin.mylibrary.repos;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.zinin.mylibrary.domain.Book;

import java.util.List;

public interface BookRepo extends JpaRepository<Book, Long> {
    List<Book> findByAuthor(String author);
    List<Book> findByBookname(String bookname);
}
